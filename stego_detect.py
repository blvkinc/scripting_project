import logging
from PIL import Image
import os
import argparse

# --- Stage 1: Header Validation ---
def check_header(filepath):
    '''
    Extracts hexadecimal values from headers to identify spoofed file types.
    '''
    try:
        file = open(filepath, 'rb')
        d = file.read(8) 
        file.close()
        h = d.hex()
        if h == "89504e470d0a1a0a":
            logging.info("valid PNG")
        elif h.startswith("ffd8ffe0") or h.startswith("ffd8ffee"):
            logging.info("valid JPEG")
        else:
            logging.info("Warning: Header mismatch or unknown file type!")
        return d
    except Exception as e:
        logging.error(f"Failed to read headers: {e}")

# --- Stage 2: Structural Analysis ---
def analyze_structure(filepath):
    '''
    Calculates the gradient of every individual pixel to identify structural anomalies.
    '''
    try:
        img = Image.open(filepath)
        pixels = img.load()
        width, height = img.size
        anomalies = 0
        for x in range(width):
            for y in range(height):
                p = pixels[x, y]
                if x < width - 1:
                    right_pixel = pixels[x+1, y]
                    if isinstance(p, int):
                        diff = abs(p - right_pixel)
                    else:
                        diff = abs(p[0] - right_pixel[0])
                    if diff > 100:
                        anomalies += 1
        if anomalies > 500:
            logging.info(f"Structural anomalies detected! Found {anomalies} sharp gradients.")
        else:
            logging.info(f"Structure looks okay.")
    except Exception as e:
        logging.error(f"Pillow failed to analyze structure: {e}")

# --- Stage 3: Payload Extraction ---
def extract_lsb(filepath):
    '''
    Extracts the Least Significant Bit (LSB) from the red channel of the image.
    This helps identify steganographic payloads hiding in the noise floor of the image.
    '''
    try:
        img = Image.open(filepath)
        pixels = img.load()
        bits = []
        for y in range(img.height):
            for x in range(img.width):
                p = pixels[x,y]
                if isinstance(p, tuple):
                    bits.append(str(p[0] & 1))
                else:
                    bits.append(str(p & 1))
                if len(bits) >= 800:
                    break
            if len(bits) >= 800:
                break
        
        bytes_data = ["".join(bits[i:i+8]) for i in range(0, len(bits), 8)]
        ascii_text = ""
        for b in bytes_data:
            val = int(b, 2)
            if 32 <= val <= 126:
                ascii_text += chr(val)
            else:
                ascii_text += "." 
        logging.debug(f"Raw LSB decoded sample: {ascii_text}")
        alphanumeric = sum(c.isalnum() for c in ascii_text)
        if alphanumeric > 20: 
            logging.info("WARNING: Potential steganographic payload detected in LSB!")
        else:
            logging.info("No obvious LSB payloads detected.")
    except Exception as e:
        logging.error(f"Failed LSB extraction: {e}")

def setup_logger(verbose, out_file):
    lvl = logging.DEBUG if verbose else logging.INFO
    handlers = [logging.StreamHandler()]
    if out_file:
        handlers.append(logging.FileHandler(out_file))
    logging.basicConfig(level=lvl, format='%(levelname)s: %(message)s', handlers=handlers)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-v', '--verbose', action='store_true')
    p.add_argument('-o', '--output', default=None)
    
    args = p.parse_args()

    setup_logger(args.verbose, args.output)
    logging.info(f"--- Starting Analysis on {args.input} ---")
    if not os.path.exists(args.input):
        logging.error(f"File {args.input} does not exist.")
        return

    check_header(args.input)
    analyze_structure(args.input)
    extract_lsb(args.input)

if __name__ == '__main__':
    main()

from PIL import Image
import argparse

def check_header(filepath):
    try:
        file = open(filepath, 'rb')
        d = file.read(8) 
        file.close()
        h = d.hex()
        if h == "89504e470d0a1a0a":
            print("valid PNG")
        elif h.startswith("ffd8ffe0") or h.startswith("ffd8ffee"):
            print("valid JPEG")
        else:
            print("Warning: Header mismatch or unknown file type!")
        return d
    except Exception as e:
        print("error:", e)

def analyze_structure(filepath):
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
            print(f"Structural anomalies detected! Found {anomalies} sharp gradients.")
        else:
            print(f"Structure looks okay.")
    except Exception as e:
        print("pillow error:", e)

def extract_lsb(filepath):
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
        print("lsb:", ascii_text)
    except Exception as e:
        print("lsb error:", e)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-v', '--verbose', action='store_true')
    
    args = p.parse_args()

    if args.verbose:
        print("verbose is on")
        print("file:", args.input)

    check_header(args.input)
    analyze_structure(args.input)
    extract_lsb(args.input)

if __name__ == '__main__':
    main()

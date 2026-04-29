from PIL import Image, ImageDraw

def create_benign_image():
    img = Image.new('RGB', (100, 100), color = 'blue')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 80, 80], fill='lightblue')
    img.save('benign.png')
    print("Created benign.png")

def create_stego_image():
    # start with a red image
    img = Image.new('RGB', (100, 100), color = 'red')
    pixels = img.load()
    
    # payload to hide
    payload = "SECRET_PAYLOAD_THIS_IS_A_TEST_OF_LSB_EXTRACTION"
    bits = ''.join(format(ord(c), '08b') for c in payload)
    
    # pad to 800 bits to match the reader's extraction length if we want, or just let it read noise
    # inject into red channel LSB
    bit_idx = 0
    for y in range(img.height):
        for x in range(img.width):
            if bit_idx < len(bits):
                r, g, b = pixels[x, y]
                # clear LSB and set to payload bit
                r = (r & ~1) | int(bits[bit_idx])
                pixels[x, y] = (r, g, b)
                bit_idx += 1
                
            # let's also create a sharp gradient anomaly artificially
            if y == 50 and x > 10 and x < 90:
                pixels[x, y] = (0, 0, 0) # sudden black line
                
    img.save('stego.png')
    print("Created stego.png")

if __name__ == '__main__':
    create_benign_image()
    create_stego_image()

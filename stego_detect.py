import argparse

def get_data(filepath):
    try:
        file = open(filepath, 'rb')
        d = file.read(8) 
        file.close()
        h = d.hex()
        if h == "89504e470d0a1a0a":
            print("valid PNG")
        else:
            print("NOT a png, might be spoofed")
        return d
    except Exception as e:
        print("error:", e)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-v', '--verbose', action='store_true')
    
    args = p.parse_args()

    if args.verbose:
        print("verbose is on")
        print("file:", args.input)

    res = get_data(args.input)

if __name__ == '__main__':
    main()

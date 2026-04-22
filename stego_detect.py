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

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', required=True)
    p.add_argument('-v', '--verbose', action='store_true')
    
    args = p.parse_args()

    if args.verbose:
        print("verbose is on")
        print("file:", args.input)

    res = check_header(args.input)

if __name__ == '__main__':
    main()

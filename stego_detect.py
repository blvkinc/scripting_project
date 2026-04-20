import argparse

def get_data(filepath):
    try:
        file = open(filepath, 'r')
        d = file.read(100) 
        file.close()
        print(f"read ok: {filepath}")
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

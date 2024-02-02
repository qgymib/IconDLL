import argparse
import icondll.core

def main():
    """
    A function to parse command line arguments and print the 'path' attribute of the parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", action='append', help="input file", required=True)
    parser.add_argument("-o", type=str, help="output file", required=True)
    args = parser.parse_args()
    print(args.i)
    icondll.core.create_dll_from_ico(args.i, args.o)

if __name__ == "__main__":
    main()

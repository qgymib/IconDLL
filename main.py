from PIL import Image
from pathlib import Path
import argparse
import icondll.core
import zipfile
import tempfile
import os

def process_img(tmpdir, idx, input_file, icons):
    """
    A function to process an image by creating a temporary directory for the input file, converting the image to .ico format, and adding the .ico to the list of icons. 

    Parameters:
    - tmpdir: The temporary directory path
    - idx: The index of the image
    - input_file: The path of the input image file
    - icons: The list of icons

    Return:
    This function does not return anything.
    """
    # Create a temporary directory for the input file.
    abs_cwd_path = os.path.abspath(tmpdir + '/input_' + str(idx))
    os.mkdir(abs_cwd_path)
    # Convert to .ico
    file_name = Path(input_file).stem
    img = Image.open(input_file)
    abs_dst_path = os.path.abspath(abs_cwd_path + '/' + file_name + '.ico')
    img.save(abs_dst_path, 'ico')
    # Add the .ico to the list of icons
    process_input(tmpdir, idx, abs_dst_path, icons)

def process_ico(tmpdirname, idx, input_file, icons):
    """
    This function processes the input file and appends it to the icons list.

    Parameters:
    - tmpdir: The temporary directory path
    - idx: The index of the image
    - input_file: The path of the input image file
    - icons: The list of icons

    Return:
    This function does not return anything.
    """
    icons.append(input_file)

def handle_unknown_filetype(tmpdirname, idx, input_file, icons):
    """
    Handle unknown filetype and raise an exception.

    Args:
        tmpdirname (str): The temporary directory name.
        idx (int): The index of the file.
        input_file (str): The input file name.
        icons (list): The list of icons.

    Raises:
        Exception: If the filetype is unknown.
    """
    ext = os.path.splitext(input_file)[1]
    raise Exception(f"Unknown filetype: {ext}")

def process_input(tmpdirname, idx, input_file, icons):
    ext_map = {
        '.png': process_img,
        '.ico': process_ico,
    }
    ext = os.path.splitext(input_file)[1]
    ext_map.get(ext, handle_unknown_filetype)(tmpdirname, idx, input_file, icons)

def main():
    """
    A function to parse command line arguments and print the 'path' attribute of the parsed arguments.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", action='append', help="input file", required=True)
    parser.add_argument("-o", type=str, help="output file", required=True)
    args = parser.parse_args()
    # Process input files
    icons = []
    with tempfile.TemporaryDirectory() as tmpdir:
        for i,file in enumerate(args.i, start=1):
            process_input(tmpdir, i, file, icons)
        icondll.core.create_dll_from_ico(tmpdir, icons, args.o)

if __name__ == "__main__":
    main()

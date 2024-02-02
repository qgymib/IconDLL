from PIL import Image
import argparse
import icondll.core
import subprocess
import hashlib
import tempfile
import os

def get_file_sha1(path):
    """
    Calculate the SHA-1 hash of the file located at the given path.

    Parameters:
    path (str): The path to the file.

    Returns:
    str: The SHA-1 hash of the file.
    """
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def process_img(tmpdir, input_file, icons):
    """
    A function to process an image by converting the image to .ico format, and adding the .ico to the list of icons. 

    Parameters:
    - tmpdir: The temporary directory path
    - input_file: The path of the input image file
    - icons: The list of icons

    Return:
    This function does not return anything.
    """
    # Convert to .ico
    img = Image.open(input_file)
    abs_dst_path = os.path.abspath(tmpdir + '/' + get_file_sha1(input_file) + '.ico')
    img.save(abs_dst_path, 'ico')
    # Add the .ico to the list of icons
    process_input(tmpdir, abs_dst_path, icons)

def process_svg(tmpdir, input_file, icons):
    """
    Convert .svg to .ico
    """
    abs_dst_path = os.path.abspath(tmpdir + '/' + get_file_sha1(input_file) + '.ico')
    subprocess.run([r'bin\svg_to_ico.exe', '-i', input_file, '-o', abs_dst_path], check=True)
    process_input(tmpdir, abs_dst_path, icons)

def process_ico(tmpdirname, input_file, icons):
    """
    This function processes the input file and appends it to the icons list.

    Parameters:
    - tmpdir: The temporary directory path
    - input_file: The path of the input image file
    - icons: The list of icons

    Return:
    This function does not return anything.
    """
    icons.append(input_file)

def handle_unknown_filetype(tmpdirname, input_file, icons):
    """
    Handle unknown filetype and raise an exception.

    Args:
        tmpdirname (str): The temporary directory name.
        input_file (str): The input file name.
        icons (list): The list of icons.

    Raises:
        Exception: If the filetype is unknown.
    """
    ext = os.path.splitext(input_file)[1]
    raise Exception(f"Unknown filetype: {ext}")

def process_input(tmpdirname, input_file, icons):
    ext_map = {
        '.svg': process_svg,
        '.png': process_img,
        '.ico': process_ico,
    }
    ext = os.path.splitext(input_file)[1]
    ext_map.get(ext, handle_unknown_filetype)(tmpdirname, input_file, icons)

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
        for file in args.i:
            file = os.path.abspath(file)
            process_input(tmpdir, file, icons)
        icondll.core.create_dll_from_ico(tmpdir, icons, args.o)

if __name__ == "__main__":
    main()

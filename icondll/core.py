from PIL import Image
from typing import List

import os
import subprocess
import tempfile

def _generate_rc_file(icon_files: List[str], rc_file_path: str) -> None:
    """
    Generate a .rc resource file from a list of .ico files.

    Args:
    icon_files (List[str]): List of .ico file paths. It must in Windows style.
    rc_file_path (str): Path to the .rc resource file. It must in Windows style.

    Returns:
    None
    """
    with open(rc_file_path, 'w') as rc_file:
        for i, icon_file in enumerate(icon_files, start=1):
            icon_name = icon_file.replace('\\', '\\\\')
            rc_file.write(f'IDI_ICON{i} ICON "{icon_name}"\n')

def _compile_resources(rc_file_path, res_file_path):
    """
    Compile the .rc resource file into a .res file.

    Args:
    rc_file_path (str): Path to the .rc resource file.
    res_file_path (str): Path to the .res resource file.

    Returns:
    None
    """
    subprocess.run(['rc.exe', '/fo', res_file_path, rc_file_path], check=True)

def _create_dll(res_file_path, dll_path):
    """
    Create a .dll file from a .res file.

    Args:
    res_file_path (str): Path to the .res resource file.
    dll_path (str): Path to the .dll file.

    Returns:
    None
    """
    subprocess.run(['link.exe', '/dll', '/noentry', '/out:' + dll_path, res_file_path], check=True)

def create_dll_from_ico(icon_files: List[str], output_file_path: str) -> None:
    """
    Create an icon .dll file from a list of .ico files.

    Args:
    icon_files (List[str]): List of icon file paths.
    output_file_path (str): Path to the output .dll file.

    Returns:
    None
    """
    # Convert to absolute paths for better handling.
    abs_icon_files = [os.path.abspath(path) for path in icon_files]
    abs_output_file_path = os.path.abspath(output_file_path)
    # Working in a temporary directory so things can be cleaned up.
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Generate a .rc resource file.
        rc_file_path = os.path.abspath(tmpdirname + '/icon.rc')
        _generate_rc_file(abs_icon_files, rc_file_path)
        # Compile the .rc resource file into a .res file.
        res_file_path = os.path.abspath(tmpdirname + '/icon.res')
        _compile_resources(rc_file_path, res_file_path)
        # Create a .dll file from the .res file.
        _create_dll(res_file_path, abs_output_file_path)

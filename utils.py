"""
Utility functions for resource path resolution and output folder management.
"""

import sys
import os


def resource_path(relative_path):
    """
    Get the absolute path to a resource.
    Works both in normal Python execution and inside a PyInstaller bundle.
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_output_folder(folder_name="WriterReducer Output"):
    """
    Returns the path to a folder on the user's Desktop, creating it if it doesn't exist.
    """
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_path = os.path.join(desktop_path, folder_name)
    os.makedirs(output_path, exist_ok=True)
    return output_path

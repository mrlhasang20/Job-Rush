import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        print(f"Base path: {base_path}")  # Debug print
        full_path = os.path.join(base_path, relative_path)
        print(f"Full path: {full_path}")  # Debug print
        return full_path
    except Exception as e:
        print(f"Error in resource_path: {e}")
        return relative_path

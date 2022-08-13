import os
import platform
import subprocess


def open_file(path: str):
    if platform.system() == "Darwin":  # macOS
        subprocess.call(("open", path))
    elif platform.system() == "Windows":  # Windows
        os.startfile(path)
    return None

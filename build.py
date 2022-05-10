import sys
from subprocess import Popen
from shutil import make_archive


def create_bat():
    # Create .bat file
    with open("dist\\nunnix-manga.bat", "w") as f:
        f.write("start Nunnix-Manga\\Nunnix-Manga.exe\n")


def create_zip() -> None:
    # Create .zip file
    if len(sys.argv) > 1 and (sys.argv[1] == "--zip" or sys.argv[1] == "-z"):
        make_archive("nunnix-manga", "zip", "dist")


def get_base_args() -> list:
    # Command line arguments
    command = [
        "pyinstaller", "app/main.py",
        "--clean",
        "--noconfirm",
        "--name", "Nunnix-Manga",
        "--hidden-import", "bs4",
        "--exclude-module", "pytest",
        "--exclude-module", "pytest-asyncio",
        "--icon", "NONE"
    ]
    return command


def get_windows_args() -> list:
    # Command line arguments for Windows
    command = get_base_args()
    command.extend([
        "--noconsole",
        "--add-data", "app/core;core",
        "--add-data", "app/ui;ui",
        "--add-data", "app/resources;resources"
    ])
    return command


def get_linux_args() -> list:
    # Command line arguments for Linux
    command = get_base_args()
    command.extend([
        "--add-data", "app/core:core",
        "--add-data", "app/ui:ui",
        "--add-data", "app/resources:resources"
    ])
    return command


def build_windows() -> None:
    # Build for Windows
    command = get_windows_args()
    Popen(command).communicate()  # Run command
    create_bat()
    create_zip()  # Create .zip file if --zip or -z is passed


def build_linux() -> None:
    # Build for Linux
    command = get_linux_args()
    Popen(command).communicate()  # Run command
    create_zip()  # Create .zip file if --zip or -z is passed


if __name__ == "__main__":
    if sys.platform == "win32":
        build_windows()
    elif sys.platform == "linux":
        build_linux()
    else:
        print("Unsupported platform")

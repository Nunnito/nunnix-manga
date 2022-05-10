import shutil
import sys
import os

from urllib.request import urlretrieve
from subprocess import Popen
from shutil import make_archive


class CreateAppImage:
    @classmethod
    def convert_to_appimage(self) -> None:
        # Convert to AppImage
        if "--appimage" in sys.argv:
            self.download_appimagetool()
            self.create_desktop_file()
            self.copy_icon()
            self.rename_bash_file("nunnix-manga.sh", "AppRun")

            Popen(
                ["./appimagetool.AppImage", "dist"]
            ).communicate()

            if "--clean" in sys.argv:
                self.clean_up()

    @classmethod
    def download_appimagetool(self) -> None:
        if os.path.exists("appimagetool.AppImage"):
            return

        # Download AppImageTool
        urlretrieve(
            "https://github.com/AppImage/AppImageKit/releases/download/13/" +
            "appimagetool-x86_64.AppImage",
            "appimagetool.AppImage")

        # Make executable
        os.chmod("appimagetool.AppImage", 0o755)

    @classmethod
    def create_desktop_file(self) -> None:
        # Create .desktop file
        content = "[Desktop Entry]\n"
        content += "Name=Nunnix-Manga\n"
        content += "Exec=AppRun\n"
        content += "Icon=icon\n"
        content += "Type=Application\n"
        content += "Categories=Utility;Graphics;\n"

        with open("dist/nunnix-manga.desktop", "w") as f:
            f.write(content)

    @classmethod
    def copy_icon(self, name: str = "icon.svg") -> None:
        # Copy icon
        shutil.copy(
            "dist/Nunnix-Manga/resources/icons/app.svg",
            f"dist/{name}")

    @classmethod
    def rename_bash_file(self, target, new_name) -> None:
        # Rename bash file
        os.rename(f"dist/{target}", f"dist/{new_name}")

    @classmethod
    def clean_up(self) -> None:
        # Clean up AppImage files
        os.remove("appimagetool.AppImage")
        os.remove("dist/nunnix-manga.desktop")
        os.remove("dist/icon.svg")
        self.rename_bash_file("AppRun", "nunnix-manga.sh")


def create_bat():
    # Create .bat file
    with open("dist\\nunnix-manga.bat", "w") as f:
        f.write("start Nunnix-Manga\\Nunnix-Manga.exe\n")


def create_bash() -> None:
    # Create .sh file
    content = '#!/bin/bash\n'
    content += 'HERE="$(dirname "$(readlink -f "${0}")")"\n'
    content += 'exec "$HERE/Nunnix-Manga/Nunnix-Manga" "$@"\n'

    with open("dist/nunnix-manga.sh", "w") as f:
        f.write(content)

    # Make executable
    os.chmod("dist/nunnix-manga.sh", 0o755)


def create_zip() -> None:
    # Create .zip file
    if len(sys.argv) > 1 and sys.argv[1] == "--zip":
        make_archive("nunnix-manga", "zip", "dist")


def clean_up() -> None:
    # Clean up build files
    if "--clean" in sys.argv:
        shutil.rmtree("build")
        os.remove("Nunnix-Manga.spec")


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
    clean_up()  # Clean up build files if --clean is passed


def build_linux() -> None:
    # Build for Linux
    command = get_linux_args()
    Popen(command).communicate()  # Run command
    create_bash()
    # Convert to AppImage if --appimage is passed
    CreateAppImage.convert_to_appimage()
    create_zip()  # Create .zip file if --zip or -z is passed
    clean_up()  # Clean up build files if --clean is passed


if __name__ == "__main__":
    if sys.platform == "win32":
        build_windows()
    elif sys.platform == "linux":
        build_linux()
    else:
        print("Unsupported platform")

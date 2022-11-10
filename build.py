import sys
import os
import shutil
from pathlib import Path
from urllib.request import urlretrieve
from subprocess import Popen

from cx_Freeze import setup, Executable, build


class CreateZipFile(build):
    """Create a zip file with the executable and the resources"""
    description = "Create a zip file with the executable and the resources"

    def run(self):
        print("Creating zip file...")
        shutil.make_archive("nunnix-manga", "zip", "build")
        print("Zip file created")


class RemoveBloatFiles(build):
    """Remove unnecessary files from the executable"""
    description = "Remove unnecessary files from the executable"

    def run(self):
        if sys.platform == "win32":
            self.remove_windows_bloat()
        elif sys.platform == "linux":
            self.remove_linux_bloat()

    def remove_windows_bloat(self):
        # Remove PyQt5 dlls (very WIP, may not work)
        qt_files = ["Qt5Qml.dll", "Qt5Gui.dll", "Qt5Designer.dll",
                    "Qt5Location.dll", "Qt5Widgets.dll", "Qt5XmlPatterns.dll",
                    "Qt5Quick3DRuntimeRender.dll", "libeay32.dll",
                    "opengl32sw.dll", "d3dcompiler_47.dll", "libGLESv2.dll"]

        os.chdir("build/lib/PyQt5/Qt5/bin")  # Change dir to the PyQt5 folder
        for file in qt_files:
            print(f"Removing {file}...")
            os.remove(file)
        os.chdir(Path(__file__).parent)  # Change dir back to the main folder

    def remove_linux_bloat(self):
        # Remove PyQt5 .so (very WIP, may not work)
        qt_files = ["libQt5PrintSupport.so.5", "libQt5Help.so.5",
                    "libQt5Bluetooth.so.5", "libQt5Multimedia.so.5",
                    "libQt5Location.so.5", "libQt5XmlPatterns.so.5",
                    "libQt5Designer.so.5"]

        os.chdir("build/lib/PyQt5/Qt5/lib")  # Change dir to the PyQt5 folder
        for file in qt_files:
            print(f"Removing {file}...")
            os.remove(file)
        os.chdir(Path(__file__).parent)  # Change dir back to the main folder


class MakeAppImage(build):
    """Create an .appimage with the resources"""
    description = "Create an .appimage with the resources"

    def run(self):
        self.download_appimagetool()
        self.create_desktop_file()
        self.copy_icon()
        self.create_apprun()
        Popen(["./appimagetool.AppImage", "build"]).communicate()

    def download_appimagetool(self) -> None:
        # Download AppImageTool
        print("Downloading AppImageTool...")
        urlretrieve(
            "https://github.com/AppImage/AppImageKit/releases/download/13/" +
            "appimagetool-x86_64.AppImage",
            "appimagetool.AppImage")

        # Make executable
        os.chmod("appimagetool.AppImage", 0o755)

    def create_desktop_file(self) -> None:
        # Create .desktop file
        print("Creating .desktop file...")
        content = "[Desktop Entry]\n"
        content += "Name=Nunnix-Manga\n"
        content += "Exec=AppRun\n"
        content += "Icon=icon\n"
        content += "Type=Application\n"
        content += "Categories=Utility;Graphics;\n"

        with open("build/nunnix-manga.desktop", "w") as f:
            f.write(content)

    def copy_icon(self, name: str = "icon.svg") -> None:
        # Copy app icon
        print("Copying icon...")
        shutil.copy("app/resources/icons/app.svg", f"build/{name}")

    def create_apprun(self) -> None:
        # Create AppRun file
        print("Creating AppRun file...")
        content = '#!/bin/bash\n'
        content += 'HERE="$(dirname "$(readlink -f "${0}")")"\n'
        content += 'exec "$HERE/Nunnix-Manga" "$@"\n'

        with open("build/AppRun", "w") as f:
            f.write(content)

        # Make executable
        os.chmod("build/AppRun", 0o755)


class CleanUp(build):
    """Clean up AppImage files"""
    description = "Clean up AppImage files"

    def run(self):
        # Clean up AppImage files
        print("Cleaning up...")
        os.remove("appimagetool.AppImage")
        os.remove("build/nunnix-manga.desktop")
        os.remove("build/icon.svg")
        os.remove("build/AppRun")


base = "Win32GUI" if sys.platform == "win32" else None

build_exe_options = {
    "build_exe": "build",
    "packages": ["bs4"],
    "excludes": ["tkinter", "test", "pytest", "soupsieve"],
    "include_files": [
        ("app/core/", "lib/core/"),
        ("app/ui/", "lib/ui/"),
        ("app/resources/", "lib/resources/"),
    ],
    "optimize": 2
}

setup(
    name="Nunnix-Manga",
    version="0.1",
    description="Manga reader",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "app/main.py",
            target_name="Nunnix-Manga",
            base=base,
            icon=None if sys.platform == "linux"
            else "app/resources/icons/app.ico"
        )
    ],
    cmdclass={
        "remove_bloat": RemoveBloatFiles,
        "zip": CreateZipFile,
        "appimage": MakeAppImage,
        "clean": CleanUp
    },
)

import sys
import os
import shutil
from pathlib import Path
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


base = "Win32GUI" if sys.platform == "win32" else None

build_exe_options = {
    "build_exe": "build",
    "packages": ["bs4"],
    "excludes": ["tkinter", "test", "pytest"],
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
            icon="app/resources/icons/app.ico"
        )
    ],
    cmdclass={
        "remove_bloat": RemoveBloatFiles,
        "zip": CreateZipFile
    },
)

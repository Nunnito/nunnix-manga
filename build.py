import sys
from subprocess import Popen


command = [
    sys.executable, "-m", "nuitka", "app/main.py",
    "--show-progress",
    "--onefile",
    "--plugin-enable=pyqt5",
    "--assume-yes-for-downloads",
    "--include-data-dir=app/core=core",
    "--include-data-dir=app/ui=ui",
    "--include-data-dir=app/resources=resources",
    "--show-progress",
    "--nofollow-import-to=core",
    "--include-package=bs4",
    "--include-qt-plugins=sensible,qml",
    "--remove-output"
]

if sys.platform == "linux":
    command.append("--linux-onefile-icon=app/resources/icons/app.svg")
    command.append("-o Nunnix-Manga.bin")

Popen(command)

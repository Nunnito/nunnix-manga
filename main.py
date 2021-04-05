from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication
from pathlib import Path
from os import environ
from nunnix_manga.utils import settings
import sys

# Set environment variables
environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

# Set init variables
application = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

# Load QML file and execute it
engine.load(str(Path(__file__).parent / "nunnix_manga" / "qml" / "main.qml"))
sys.exit(application.exec_())

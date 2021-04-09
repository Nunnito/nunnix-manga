from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication
from pathlib import Path
from os import environ
from app.utils import settings
import sys

# Set environment variables
environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

# Set init variables
application = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
context = engine.rootContext()

# Load variables to QML
context.setContextProperty("thm", settings.get_theme_file_content())  # Theme

# Load QML file and execute it
engine.load(str(Path(__file__).parent / "app" / "ui" / "main.qml"))
sys.exit(application.exec_())

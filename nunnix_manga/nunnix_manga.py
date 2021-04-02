from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication
import sys
import os

# Set environment variables
os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

# Set init variables
application = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

# Load QML file and execute it
engine.load(os.path.join(os.path.dirname(__file__), "qml/main.qml"))
sys.exit(application.exec_())

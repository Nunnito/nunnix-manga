from core.utils.get_icon import Icon
from core.utils import settings

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from pathlib import Path
from os import environ
import sys


def before_close():
    """Actions before the application exits"""
    del globals()["engine"]


# Set environment variables
environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

# Set init variables
application = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
context = engine.rootContext()

# Load variables to QML
icon_engine = Icon()
context.setContextProperty("thm", settings.get_theme_file_content())  # Theme
context.setContextProperty("Icon", icon_engine)

# Set application properties
application.aboutToQuit.connect(before_close)
application.setWindowIcon(QIcon(icon_engine.get_icon("app.svg")))

# Load QML file and execute it
engine.load(str(Path(__file__).parent / "ui" / "main.qml"))
sys.exit(application.exec_())

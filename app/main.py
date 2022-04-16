import sys
from os import environ
from pathlib import Path

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon

from core.utils import qml_utils

# Set init variables
application = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
context = engine.rootContext()


def before_close():
    """Actions before the application exits"""
    del globals()["engine"]


def main():
    # Set environment variables
    environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

    # Load variables to QML
    icon_engine = qml_utils.Icon()
    theme_engine = qml_utils.Theme()
    context.setContextProperty("Icon", icon_engine)
    context.setContextProperty("Theme", theme_engine)

    # Set application properties
    application.aboutToQuit.connect(before_close)
    application.setWindowIcon(QIcon(icon_engine.get_icon("app.svg")))

    # Load QML file and execute it
    engine.load(str(Path(__file__).parent / "ui" / "main.qml"))
    sys.exit(application.exec_())


if __name__ == "__main__":
    main()

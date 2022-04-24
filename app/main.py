import asyncio
import sys

from pathlib import Path
from os import environ
import warnings

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication, QIcon
from aiohttp import ClientSession
from qasync import QEventLoop

from core.utils import qml_utils
from core.types import Scraper

# Set init variables
application = QGuiApplication(sys.argv)
loop = QEventLoop(application)
asyncio.set_event_loop(loop)
engine = QQmlApplicationEngine()
context = engine.rootContext()

# Create session and suppress its warning
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    session = ClientSession(loop=loop)


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
    scraper_engine = Scraper(session)
    context.setContextProperty("Icon", icon_engine)
    context.setContextProperty("Theme", theme_engine)
    context.setContextProperty("Scraper", scraper_engine)

    # Set application properties
    application.aboutToQuit.connect(before_close)
    application.setWindowIcon(QIcon(icon_engine.get_icon("app.svg")))

    # Load QML file and execute it
    engine.load(str(Path(__file__).parent / "ui" / "main.qml"))
    with loop:
        loop.run_forever()
        loop.create_task(session.close())


if __name__ == "__main__":
    main()

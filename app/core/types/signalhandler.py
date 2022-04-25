from PyQt5.QtCore import QObject, pyqtSignal
from core.types import Manga


class SignalHandler(QObject):
    """ Signal handler to emit signals """
    mangaSearch = pyqtSignal(list)
    mangaData = pyqtSignal(Manga)
    chapterImages = pyqtSignal(list)

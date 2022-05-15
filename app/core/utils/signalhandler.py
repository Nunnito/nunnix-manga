from PyQt5.QtCore import QObject, QVariant, pyqtSignal
from ..types import Manga


class SignalHandler(QObject):
    """ Signal handler to emit signals """
    mangaSearch = pyqtSignal(QVariant)
    mangaData = pyqtSignal(Manga)
    chapterImages = pyqtSignal(QVariant)

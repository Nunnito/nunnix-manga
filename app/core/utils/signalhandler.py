from PyQt5.QtCore import QObject, QVariant, pyqtSignal


class SignalHandler(QObject):
    """ Signal handler to emit signals """
    searchResult = pyqtSignal(QVariant)
    contentData = pyqtSignal(QVariant)
    chapterImages = pyqtSignal(QVariant)

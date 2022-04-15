from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSlot


class Icon(QObject):
    """This class will be used in QML for simple access to icons"""

    @pyqtSlot(str, result=str)
    def get_icon(self, icon: str) -> str:
        """Get icon absolute path

        Args:
            icon (str): Icon name

        Returns:
            str: Icon absolute path (even if it doesn't exist)
        """
        return str(Path(__file__).parents[2] / "resources" / "icons" / icon)

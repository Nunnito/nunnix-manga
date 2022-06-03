from pathlib import Path
from PyQt5.QtCore import QObject, QVariant, pyqtSlot

from . import python_utils
from ..modules import DataExplorer
from ..types import Manga


class Icon(QObject):
    """This class will be used in QML for simple access to icons"""

    @pyqtSlot(str, result=str)
    def get_icon(self, icon: str, uri: bool = True) -> str:
        """Get icon absolute path

        Args:
            icon (str): Icon name

        Returns:
            str: Icon absolute path (even if it doesn't exist)
        """
        if uri:
            return (Path(__file__).parents[2]/"resources"/"icons" /
                    icon).as_uri()
        else:
            return str(Path(__file__).parents[2]/"resources"/"icons"/icon)


class Theme(QObject):
    """This class will be used in QML to get the current theme"""

    @pyqtSlot(QObject, QObject, result=QVariant)
    def get_theme(self, dark: QObject, light: QObject) -> QVariant:
        """Get current theme

        Returns:
            str: Current theme
        """
        theme = python_utils.Paths.get_theme_file_content()
        dark_theme = qobject_to_dict(dark)
        dark_theme.update(theme)
        theme = dark_theme

        return theme


class Cast(QObject):
    """This class will be used in QML to cast an object to other type"""
    @pyqtSlot(Manga, result=DataExplorer)
    def from_manga(self, manga: Manga) -> DataExplorer:
        """Cast Manga to DataExplorer

        Args:
            manga (Manga): Manga object

        Returns:
            DataExplorer: DataExplorer object
        """
        return DataExplorer(manga)


def qobject_to_dict(qobject: QObject) -> dict:
    """Convert a QObject to a dict

    Args:
        qbject (QObject): QObject to convert

    Returns:
        dict: Converted QObject
    """
    result = {}
    meta_object = qobject.metaObject()

    for i in range(meta_object.propertyOffset(), meta_object.propertyCount()):
        property = meta_object.property(i)
        result[property.name()] = qobject.property(property.name())
    return result

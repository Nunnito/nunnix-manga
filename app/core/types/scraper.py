import os
from PyQt5.QtCore import QObject, QVariant, QJsonValue, pyqtSlot, pyqtProperty
from importlib import import_module
from pathlib import Path

from core import scrapers
from core.types import MangaSearch


class Scraper(QObject):
    def __init__(self, parent=None) -> None:
        super(Scraper, self).__init__(parent)

        self._scrapers_list = self.get_scrapers()
        self._scraper = self._scrapers_list[0]

    # Get as input a dict with all parameters to search
    @pyqtSlot(QJsonValue, result=QVariant)
    def search_manga(self, params: QJsonValue) -> list[MangaSearch]:
        params = params.toVariant()
        data = self._scraper.search_manga(**params)

        results = []
        for result in data:
            title = result["title"]
            link = result["link"]
            cover = result["cover"]
            results.append(MangaSearch(self._scraper, title, link, cover,
                                       self))

        return results

    @pyqtProperty(QVariant)
    def scraper(self) -> object:
        return self._scraper

    @scraper.setter
    def scraper(self, scraper: str) -> None:
        for class_obj in self._scrapers_list:
            if class_obj.NAME == scraper:
                self._scraper = class_obj
                break

    @pyqtProperty(list)
    def scrapers_list(self) -> list:
        scrapers_list = []
        for scraper in self._scrapers_list:
            scrapers_list.append(scraper.NAME)

        return scrapers_list

    def get_scrapers(self) -> list:
        classes = []
        for file in Path(scrapers.__path__[0]).glob("*.py"):
            name = os.path.splitext(os.path.basename(file))[0]
            module = import_module(f"{scrapers.__name__}.{name}")

            for attr in dir(module):
                class_obj = getattr(module, attr)
                if hasattr(class_obj, "get_manga_data"):
                    classes.append(class_obj)

        return classes

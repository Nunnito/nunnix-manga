import os

from importlib import import_module
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtProperty
from aiohttp import ClientSession
from qasync import asyncSlot

from core.types import MangaSearch, SignalHandler
from core import scrapers


class Explorer(SignalHandler, QObject):
    def __init__(self, session: ClientSession, signals_handler: SignalHandler,
                 parent=None) -> None:
        super(Explorer, self).__init__(parent)

        self._scrapers_list = self.get_scrapers()
        self._scraper = self._scrapers_list[0]
        self._session = session
        self._signals_handler = signals_handler
        self._controls = self._scraper.advanced_search_controls()

    # Get as input a dict with all parameters to search
    @asyncSlot(str, QObject, int)
    async def search_manga(self, search_type: str, search_root: QObject,
                           page: int):
        # params = params.toVariant()
        if search_type == "empty":
            data = await self._scraper.search_manga(self._session, page=page)
        elif search_type == "title":
            title = search_root.property("text")
            data = await self._scraper.search_manga(self._session,
                                                    title=title, page=page)

        results = []
        for result in data:
            title = result["title"]
            link = result["link"]
            cover = result["cover"]
            results.append(MangaSearch(self._scraper, self._session,
                                       title, link, cover, self))

        self._signals_handler.mangaSearch.emit(results)

    @pyqtProperty(str)
    def scraper(self) -> object:
        return self._scraper.NAME

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

    @pyqtProperty(list, constant=True)
    def advanced_search(self) -> list:
        return self._controls

import os
from importlib import import_module
from pathlib import Path

from core import scrapers
from core.types import MangaSearch


class Scraper:
    def __init__(self) -> None:
        self._scrapers_list = self.get_scrapers()
        self._scraper = self._scrapers_list[0]

    def search_manga(self, **kwargs) -> list[MangaSearch]:
        data = self._scraper.search_manga(**kwargs)

        results = []
        for result in data:
            title = result["title"]
            link = result["link"]
            cover = result["cover"]
            results.append(MangaSearch(self._scraper, title, link, cover))

        return results

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

    @property
    def scraper(self) -> object:
        return self._scraper

    @scraper.setter
    def scraper(self, scraper: str) -> None:
        for class_obj in self._scrapers_list:
            if class_obj.NAME == scraper:
                self._scraper = class_obj
                break

    @property
    def scrapers_list(self) -> list:
        scrapers_list = []
        for scraper in self._scrapers_list:
            scrapers_list.append(scraper.NAME)

        return scrapers_list

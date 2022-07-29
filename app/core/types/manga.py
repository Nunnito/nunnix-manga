import time
import json
from hashlib import md5

from PyQt5.QtCore import QObject, QVariant, pyqtProperty
from qasync import asyncSlot

from .generic import SearchResult, ContentData
from ..utils import python_utils


class Chapter(QObject):
    """ Chapter type to be used in Manga class """
    def __init__(self, scraper, title: str, date: time.struct_time,
                 link: str, web_link: str, scanlation: str, parent) -> None:
        super(Chapter, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._date = date
        self._link = link
        self._web_link = web_link
        self._scanlation = scanlation
        self._parent = parent

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str, constant=True)
    def title(self) -> str:
        return self._title

    @pyqtProperty(str, constant=True)
    def date(self) -> list:
        return time.strftime('%d/%m/%Y', self._date)

    @pyqtProperty(str, constant=True)
    def link(self) -> str:
        return self._link

    @pyqtProperty(str, constant=True)
    def web_link(self) -> str:
        return self._web_link

    @pyqtProperty(str, constant=True)
    def scanlation(self) -> str:
        return self._scanlation

    @asyncSlot()
    async def get_images(self) -> None:
        """ Get images from chapter """
        images = await self._scraper.get_chapter_images(self._link)
        self._parent._parent._signals_handler.chapterImages.emit(images)


class ChaptersData(QObject):
    """ Chapters data type to be used in Manga class """
    def __init__(self, total: int, chapters: list[Chapter], parent) -> None:
        super(ChaptersData, self).__init__(parent)

        self._total = total
        self._chapters = chapters
        self._parent = parent

    @pyqtProperty(int, constant=True)
    def total(self) -> int:
        return self._total

    @pyqtProperty(QVariant, constant=True)
    def chapters(self) -> list[Chapter]:
        return self._chapters


class Manga(ContentData):
    """ Manga type to get all manga data """
    def __init__(self, scraper, title: str, author: str, description: str,
                 cover: list[str], genres: list[str], status: str, link: str,
                 web_link: str, chapters_data: ChaptersData, parent) -> None:
        super(Manga, self).__init__(scraper, title, author, description,
                                    cover, genres, link, web_link, parent)

        self._status = status
        self._chapters_data = chapters_data

    @pyqtProperty(str, constant=True)
    def status(self) -> str:
        return self._status

    @pyqtProperty(QVariant, constant=True)
    def chapters_data(self) -> ChaptersData:
        return self._chapters_data


class MangaSearch(SearchResult):
    """ Manga search type """
    def __init__(self, scraper, title: str, link: str, web_link: str,
                 cover: str, parent):
        super(MangaSearch, self).__init__(scraper, title, link, web_link,
                                          cover, parent)

    @asyncSlot()
    async def get_data(self) -> None:
        """ Get manga data """
        data = await self._create_data()

        title = data["title"]
        author = data["author"]
        description = data["description"]
        cover = data["cover"]
        genres = data["genres"]
        status = data["status"]
        chapters = []
        for chapter in data["chapters_data"]["chapters"]:
            chapters.append(
                Chapter(
                    self._scraper,
                    chapter["title"],
                    chapter["date"],
                    chapter["link"],
                    chapter["web_link"],
                    chapter["scanlation"],
                    self
                )
            )
        chapters_data = ChaptersData(data["chapters_data"]["total"], chapters,
                                     self)

        if not isinstance(cover, list):
            cover = [cover, None]

        manga = Manga(
            self._scraper,
            title, author, description, cover, genres, status, self._link,
            self._web_link, chapters_data, self
        )
        self._parent._signals_handler.contentData.emit(manga)

    def _get_saved_data(self) -> dict | None:
        # Encode title and scraper to MD5
        encode_title = md5(self.title.encode()).hexdigest()

        config_file = (python_utils.Paths.get_mangas_path() /
                       self.scraper/encode_title/f"{encode_title}.json")
        cache_file = (python_utils.Paths.get_cache_path() /
                      self.scraper/encode_title/f"{encode_title}.json")

        # If the manga is in the config folder, load it
        if config_file.exists():
            # Load from config
            with open(config_file) as f:
                data = json.load(f)
        # Else if the manga is in the cache folder, load it
        elif cache_file.exists():
            # Load from cache
            with open(cache_file) as f:
                data = json.load(f)
        # Else, return None
        else:
            data = None

        return data

    async def _create_data(self) -> dict:
        """ Retrieve manga data from different sources:
            - from config if exists
            - from cache if exists
            - from scraper if not exists
        """
        # Encode title and scraper to MD5
        encode_title = md5(self.title.encode()).hexdigest()

        config_file = (python_utils.Paths.get_mangas_path()/self.scraper /
                       encode_title/f"{encode_title}.json")
        cache_file = (python_utils.Paths.get_cache_path()/self.scraper /
                      encode_title/f"{encode_title}.json")

        data = self._get_saved_data()  # Get data from config or cache
        if data is None:  # If data is None, get it from scraper
            data = await self._scraper.get_content_data(self._link)

        if (config_file.exists() or cache_file.exists()):
            # Update chapters date
            for chapter in data["chapters_data"]["chapters"]:
                chapter["date"] = time.strptime(chapter["date"], "%d/%m/%Y")

        return data

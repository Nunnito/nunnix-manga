from PyQt5.QtCore import QObject, QVariant, pyqtProperty
from qasync import asyncSlot

from .generic import SearchResult, ContentData


class Chapter(QObject):
    """ Chapter type to be used in Manga class """
    def __init__(self, scraper, title: str, date: list[str, str, str],
                 link: str, scanlation: str, parent) -> None:
        super(Chapter, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._date = date
        self._link = link
        self._scanlation = scanlation
        self._parent = parent

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str, constant=True)
    def title(self) -> str:
        return self._title

    @pyqtProperty(list, constant=True)
    def date(self) -> list:
        return self._date

    @pyqtProperty(str, constant=True)
    def link(self) -> str:
        return self._link

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

    @pyqtProperty(int, constant=True)
    def total(self) -> int:
        return self._total

    @pyqtProperty(QVariant, constant=True)
    def chapters(self) -> list[Chapter]:
        return self._chapters


class Manga(ContentData):
    """ Manga type to get all manga data """
    def __init__(self, scraper, title: str, author: str, description: str,
                 cover: str, genres: list[str], status: str, link: str,
                 chapters_data: ChaptersData, parent) -> None:
        super(Manga, self).__init__(scraper, title, author, description,
                                    cover, genres, link, parent)

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
    def __init__(self, scraper, title: str, link: str, cover: str, parent):
        super(MangaSearch, self).__init__(scraper, title, link, cover, parent)

    @asyncSlot()
    async def get_data(self) -> None:
        """ Get manga data """
        data = await self._scraper.get_content_data(self._link)

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
                    chapter["scanlation"],
                    self
                )
            )
        chapters_data = ChaptersData(data["chapters_data"]["total"], chapters,
                                     self)

        manga = Manga(
            self._scraper,
            title, author, description, cover, genres, status, self._link,
            chapters_data, self
        )
        self._parent._signals_handler.contentData.emit(manga)

from abc import abstractmethod
from PyQt5.QtCore import QObject, QJsonValue, pyqtProperty
from qasync import asyncSlot


class SearchResult(QObject):
    def __init__(self, scraper, title: str, link: str, cover: str, parent):
        super(SearchResult, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._link = link
        self._cover = cover
        self._parent = parent

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str, constant=True)
    def title(self) -> str:
        return self._title

    @pyqtProperty(str, constant=True)
    def link(self) -> str:
        return self._link

    @pyqtProperty(str, constant=True)
    def cover(self) -> str:
        return self._cover

    @pyqtProperty(QJsonValue, constant=True)
    def jsonObject(self) -> dict:
        jsonObject = {
            "title": self._title,
            "link": self._link,
            "cover": self._cover
        }
        return jsonObject

    @abstractmethod
    @asyncSlot()
    async def get_data(self) -> None:
        pass


class ContentData(QObject):
    def __init__(self, scraper, title: str, author: str, description: str,
                 cover: list[str], genres: list[str], link: str,
                 parent) -> None:
        super(ContentData, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._author = author
        self._description = description
        self._cover = cover
        self._genres = genres
        self._link = link
        self._parent = parent

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str, constant=True)
    def title(self) -> str:
        return self._title

    @pyqtProperty(str, constant=True)
    def author(self) -> str:
        return self._author

    @pyqtProperty(str, constant=True)
    def description(self) -> str:
        return self._description

    @pyqtProperty(str, constant=True)
    def cover(self) -> str:
        """
        The first index represents the remote URL, the second index represents
        the local URL
        """
        if self._cover[1] is not None:
            return self._cover[1]
        else:
            return self._cover[0]

    @pyqtProperty(list, constant=True)
    def genres(self) -> list[str]:
        return self._genres

    @pyqtProperty(str, constant=True)
    def status(self) -> str:
        return self._status

    @pyqtProperty(str, constant=True)
    def link(self) -> str:
        return self._link

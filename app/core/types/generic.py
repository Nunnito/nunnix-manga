from abc import abstractmethod
from functools import wraps

from PyQt5.QtCore import QObject, QJsonValue, pyqtProperty
from qasync import asyncSlot

from .. import modules
from ..utils import logger


def viewer_deco(qasync_func):
    @wraps(qasync_func)
    def wrapper(func):
        @wraps(func)
        async def wrapped(self, *args, **kwargs):
            try:
                await func(self, *args, **kwargs)  # Run the function

            # If an exception is raised, do the following
            except Exception as e:
                exception_info = {"is_exception": True, "exception": {}}
                exception_info["exception"]["message"] = str(e)

                logger.error(e)
                exception_info["exception"]["type"] = "unknown_error"

                # Emit the signal with the exception info
                if not isinstance(self, modules.viewer.Viewer):
                    self._parent._signals_handler\
                        .contentData.emit(exception_info)
                else:
                    self._parent._parent._signals_handler\
                        .contentData.emit(exception_info)
        return qasync_func(wrapped)
    return wrapper


class SearchResult(QObject):
    def __init__(self, scraper, title: str, link: str, web_link: str,
                 cover: str, parent):
        super(SearchResult, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._link = link
        self._web_link = web_link
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
    def web_link(self) -> str:
        return self._web_link

    @pyqtProperty(str, constant=True)
    def cover(self) -> str:
        return self._cover

    @pyqtProperty(QJsonValue, constant=True)
    def jsonObject(self) -> dict:
        jsonObject = {
            "title": self._title,
            "link": self._link,
            "web_link": self._web_link,
            "cover": self._cover
        }
        return jsonObject

    @abstractmethod
    @asyncSlot()
    async def get_data(self) -> None:
        pass


class ContentData(QObject):
    def __init__(self, scraper, title: str, author: str, description: str,
                 cover: list[str], genres: list[str], link: str, web_link: str,
                 parent) -> None:
        super(ContentData, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._author = author
        self._description = description
        self._cover = cover
        self._genres = genres
        self._link = link
        self._web_link = web_link
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
    def link(self) -> str:
        return self._link

    @pyqtProperty(str, constant=True)
    def web_link(self) -> str:
        "Web link represents the link to the website"
        return self._web_link

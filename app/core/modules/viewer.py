import json
import time
import shutil
from hashlib import md5
from pathlib import Path

from ..types import Manga, Chapter, ChaptersData
from ..utils import python_utils

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal
from aiohttp import ClientSession
from qasync import asyncSlot


class Viewer(Manga):
    saved = pyqtSignal()  # Emitted when the content is saved

    def __init__(self, data: Manga):
        keys = locals()["data"].__dict__

        # Convert chapters type to ViewerChapter
        chapters = []
        for chapter in keys["_chapters_data"].chapters:
            chapters.append(ViewerChapter(*chapter.__dict__.values()))
        chapters_data = ChaptersDataViewer(keys["_chapters_data"]._total,
                                           chapters,
                                           keys["_chapters_data"].parent())

        self.data_dict = {
            "scraper": keys["_scraper"],
            "title": keys["_title"],
            "author": keys["_author"],
            "description": keys["_description"],
            "cover": keys["_cover"],
            "genres": keys["_genres"],
            "link": keys["_link"],
            "web_link": keys["_web_link"],
            "parent": keys["_parent"],
            "status": keys["_status"],
            "chapters_data": chapters_data,
        }

        super().__init__(**self.data_dict)

        self._session = self._parent._parent._session  # type: ClientSession
        self.chapters_data._parent = self  # Set chapters data parent to self

    @asyncSlot(bool)
    async def save(self, to_cache: bool = True):
        # Encode title and scraper to MD5
        encode_title = md5(self.title.encode()).hexdigest()

        # Create path
        if to_cache:
            path = (python_utils.Paths.get_cache_path()/f"{self.scraper}"
                    / f"{encode_title}")
        else:
            path = (python_utils.Paths.get_mangas_path()/f"{self.scraper}"
                    / f"{encode_title}")

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        file = path/f"{encode_title}.json"  # Create file

        # Convert attributes to dict
        data = {
            "scraper": self.scraper,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "cover": [self._cover[0], None],
            "genres": self.genres,
            "link": self.link,
            "web_link": self.web_link,
            "status": self.status,
            "chapters_data": {}
        }

        # Convert chapters to dict
        chapters = []
        for chapter in self.chapters_data.chapters:
            chapters.append({
                "title": chapter.title,
                "date": chapter.date,
                "link": chapter.link,
                "web_link": chapter.web_link,
                "scanlation": chapter.scanlation,
                "readed": chapter.readed,
                "bookmarked": chapter.bookmarked,
                "downloaded": chapter.downloaded
            })

        # Add chapters to data
        data["chapters_data"] = {
            "total": self.chapters_data.total,
            "chapters": chapters
        }

        # Download cover and set it to the second index positions
        thumbnail_ext = self._cover[0].split(".")[-1]  # Get the extension
        # Create MD5 hash of the thumbnail url
        thumbnail_name = f"{self.scraper}_{self._cover[0]}".encode()
        thumbnail_name = md5(thumbnail_name).hexdigest()
        thumbnail_path = path/f"{thumbnail_name}.{thumbnail_ext}"

        data["cover"][1] = None  # Set cover to None, will be set later

        # Save data
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        if not to_cache:
            self.saved.emit()

        # Download cover and set it to the second index positions
        data["cover"][1] = await self.save_image(self._cover[0],
                                                 thumbnail_path)

        # Save data with new cover
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @pyqtProperty(bool, notify=saved)
    def is_saved(self) -> bool:
        # Encode title and scraper to MD5
        encode_title = md5(self.title.encode()).hexdigest()
        config_file = (python_utils.Paths.get_mangas_path()/self.scraper /
                       encode_title/f"{encode_title}.json")

        return config_file.exists()

    @asyncSlot()
    async def remove(self) -> None:
        # Encode title and scraper to MD5
        encode_title = md5(self.title.encode()).hexdigest()

        # Create path
        path = (python_utils.Paths.get_mangas_path()/self.scraper
                / f"{encode_title}")

        # Remove path
        shutil.rmtree(path)

        self.saved.emit()

    @asyncSlot()
    async def reload(self) -> None:
        """ Reload manga data """
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
                    chapter["web_link"],
                    chapter["scanlation"],
                    self._parent
                )
            )
        chapters_data = ChaptersData(data["chapters_data"]["total"], chapters,
                                     self._parent)

        if not isinstance(cover, list):
            cover = [cover, None]

        manga = Manga(
            self._scraper,
            title, author, description, cover, genres, status, self._link,
            self._web_link, chapters_data, self._parent
        )
        self._parent._parent._signals_handler.contentData.emit(manga)

    async def save_image(self, image_url: str, path: Path) -> str | None:
        """ Save image to path """
        try:
            if not path.exists():
                await python_utils.Thumbnails.download_thumbnail(
                    image_url, path, self._session)
            return path.as_uri()
        except Exception:
            return None


class ViewerChapter(Chapter):
    selected_signal = pyqtSignal()
    readed_signal = pyqtSignal()
    bookmarked_signal = pyqtSignal()
    downloaded_signal = pyqtSignal()

    def __init__(self, scraper, title: str, date: time.struct_time, link: str,
                 web_link: str, scanlation: str, parent):
        super().__init__(scraper, title, date, link, web_link, scanlation,
                         parent)

        # New properties
        self._selected = False
        self._readed = False
        self._bookmarked = False
        self._downloaded = False

    @pyqtProperty(bool, notify=selected_signal)
    def selected(self) -> str:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        # Update selected length from parent
        if value and not self._selected:
            self._parent.selected_length += 1
        elif not value and self._selected:
            self._parent.selected_length -= 1

        self._selected = value
        self.selected_signal.emit()

    @pyqtProperty(bool, notify=readed_signal)
    def readed(self) -> str:
        return self._readed

    @readed.setter
    def readed(self, value: bool) -> None:
        self._readed = value
        self.readed_signal.emit()

    @pyqtProperty(bool, notify=bookmarked_signal)
    def bookmarked(self) -> str:
        return self._bookmarked

    @bookmarked.setter
    def bookmarked(self, value: bool) -> None:
        self._bookmarked = value
        self.bookmarked_signal.emit()

    @pyqtProperty(bool, notify=downloaded_signal)
    def downloaded(self) -> str:
        return self._downloaded

    @downloaded.setter
    def downloaded(self, value: bool) -> None:
        self._downloaded = value
        self.downloaded_signal.emit()


class ChaptersDataViewer(ChaptersData):
    selected_length_signal = pyqtSignal(int, name="selectedLength")

    def __init__(self, total: int, chapters: list[ViewerChapter], parent):
        super().__init__(total, chapters, parent)

        # New properties
        self._selected_length = 0
        self._chapters_saved_data = self._parent._get_saved_data()

        # Set chapters parent
        for chapter in self._chapters:
            chapter._parent = self

        # Set chapters data
        if self._chapters_saved_data is not None:
            saved_ch = self._chapters_saved_data["chapters_data"]["chapters"]
            for i, chapter in enumerate(self._chapters):
                chapter.readed = saved_ch[i]["readed"]
                chapter.bookmarked = saved_ch[i]["bookmarked"]
                chapter.downloaded = saved_ch[i]["downloaded"]

    @asyncSlot()
    async def select_all(self) -> None:
        for chapter in self._chapters:
            chapter.selected = True

    @asyncSlot()
    async def unselect_all(self) -> None:
        for chapter in self._chapters:
            chapter.selected = False

    @asyncSlot()
    async def mark_selected_as_readed(self) -> None:
        for chapter in self._chapters:
            if chapter.selected:
                chapter.readed = True

    @asyncSlot()
    async def unmark_selected_as_readed(self) -> None:
        for chapter in self._chapters:
            if chapter.selected:
                chapter.readed = False

    @asyncSlot()
    async def mark_selected_as_bookmarked(self) -> None:
        for chapter in self._chapters:
            if chapter.selected:
                chapter.bookmarked = True

    @asyncSlot()
    async def unmark_selected_as_bookmarked(self) -> None:
        for chapter in self._chapters:
            if chapter.selected:
                chapter.bookmarked = False

    @asyncSlot(int)
    async def mark_previous_as_read(self, index: int) -> None:
        for chapter in self._chapters[:index]:
            chapter.readed = True

    @pyqtProperty(int, notify=selected_length_signal)
    def selected_length(self) -> int:
        return self._selected_length

    @selected_length.setter
    def selected_length(self, value: int) -> None:
        self._selected_length = value
        self.selected_length_signal.emit(value)


# Class to create a new instance of the viewer
class ViewerFactory(QObject):
    @pyqtSlot(Manga, result=Viewer)
    def from_manga(self, manga: Manga) -> Viewer:
        """Cast Manga to Viewer

        Args:
            manga (Manga): Manga object

        Returns:
            Viewer: Viewer object
        """
        return Viewer(manga)

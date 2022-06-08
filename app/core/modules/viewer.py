import json
from hashlib import md5

from ..types import Manga, Chapter, ChaptersData
from ..utils import python_utils

from PyQt5.QtCore import QObject, pyqtSlot
from aiohttp import ClientSession
from qasync import asyncSlot


class Viewer(Manga):
    def __init__(self, data: Manga):
        keys = locals()["data"].__dict__
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
            "chapters_data": keys["_chapters_data"],
        }

        super().__init__(**self.data_dict)

        self._session = self._parent._parent._session  # type: ClientSession

    @asyncSlot()
    async def save_to_cache(self):
        # Encode title and scraper to MD5
        encode_title = md5(self.title.encode()).hexdigest()

        # Create path
        path = (python_utils.Paths.get_cache_path()/f"{self.scraper}"
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
                "scanlation": chapter.scanlation
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

        if not thumbnail_path.exists():
            await python_utils.Thumbnails.download_thumbnail(self._cover[0],
                                                             thumbnail_path,
                                                             self._session)
        data["cover"][1] = thumbnail_path.as_uri()

        # Save data
        with open(file, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

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

from pathlib import Path
from hashlib import md5

import asyncio
import json
import sys

from aiohttp import ClientSession

OS_NAME = sys.platform
HOME_PATH = Path.home()


class Paths:
    """
    Class that contains the directories used by the application.
    """
    @classmethod
    def get_config_file_path(cls) -> str:
        """ Returns the config file path and creates it if it doesn't exist """
        if OS_NAME == "linux":
            config_path = HOME_PATH/".config"/"nunnix-manga"/"config.json"
        if OS_NAME == "win32":
            config_path = (HOME_PATH/"AppData"/"Local"/"nunnix-manga" /
                           "config.json")

        if not config_path.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.touch()

        return config_path

    @classmethod
    def get_theme_file_path(cls) -> str:
        """ Returns the theme file path and creates it if it doesn't exist """
        if OS_NAME == "linux":
            theme_path = HOME_PATH/".config"/"nunnix-manga"/"theme.json"
        if OS_NAME == "win32":
            theme_path = (HOME_PATH/"AppData"/"Local"/"nunnix-manga" /
                          "theme.json")

        if not theme_path.exists():
            theme_path.parent.mkdir(parents=True, exist_ok=True)
            theme_path.write_text("{}")

        return theme_path

    @classmethod
    def get_theme_file_content(cls) -> dict:
        """ Returns the theme file content """
        with open(cls.get_theme_file_path()) as theme_file:
            return json.load(theme_file)

    @classmethod
    def get_thumbnails_path(cls) -> str:
        """ Returns the thumbnails dir path and creates
        it if it doesn't exist
        """
        if OS_NAME == "linux":
            path = HOME_PATH/".cache"/"nunnix-manga"/"thumbnails"
        if OS_NAME == "win32":
            path = (HOME_PATH/"AppData"/"Local"/"nunnix-manga"/"cache" /
                    "thumbnails")

        if not path.exists():
            path.mkdir(parents=True)

        return path

    @classmethod
    def get_cache_path(cls) -> str:
        """ Returns the cache dir path and creates it if it doesn't exist """
        if OS_NAME == "linux":
            path = HOME_PATH/".cache"/"nunnix-manga"/"manga"
        if OS_NAME == "win32":
            path = HOME_PATH/"AppData"/"Local"/"nunnix-manga"/"cache"/"manga"

        if not path.exists():
            path.mkdir(parents=True)

        return path

    @classmethod
    def get_mangas_path(cls) -> str:
        """ Returns the mangas dir path and creates it if it doesn't exist """
        if OS_NAME == "linux":
            path = HOME_PATH/".local"/"share"/"nunnix-manga"/"manga"
        if OS_NAME == "win32":
            path = HOME_PATH/"AppData"/"Local"/"nunnix-manga"/"manga"

        if not path.exists():
            path.mkdir(parents=True)

        return path


class Thumbnails:
    """
    Class that manages thumbnails operations.
    """

    @classmethod
    async def get_thumbnail(self, thumbnail: str, scraper: str,
                            session: ClientSession) -> str:
        """
        Get the thumbnail of a manga.

        Args:
            thumbnail (str): The thumbnail url
            scraper (str): Scraper name
            session (ClientSession): aiohttp session

        Returns:
            str: Thumbnail absolute path
        """
        thumbnail_ext = thumbnail.split(".")[-1]  # Get the extension
        # Create MD5 hash of the thumbnail url
        thumbnail_name = md5(f"{scraper}_{thumbnail}".encode()).hexdigest()
        thumbnail_path = (Paths.get_thumbnails_path() /
                          f"{thumbnail_name}.{thumbnail_ext}")

        # If the thumbnail doesn't exist, return the thumbnail url and create a
        # task to download it
        if not thumbnail_path.exists():
            asyncio.create_task(self.download_thumbnail(thumbnail,
                                                        thumbnail_path,
                                                        session))
            return thumbnail

        return thumbnail_path.as_uri()

    @classmethod
    async def download_thumbnail(self, thumbnail: str, path: Path,
                                 session: ClientSession):
        """
        Download a thumbnail.

        Args:
            thumbnail (str): The thumbnail url
            path (Path): Thumbnail path
        """
        async with session.get(thumbnail) as response:
            data = await response.read()
            path.write_bytes(data)

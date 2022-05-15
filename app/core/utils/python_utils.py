from pathlib import Path
import json
import sys

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

        return str(path)

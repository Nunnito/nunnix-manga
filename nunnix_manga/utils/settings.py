from pathlib import Path
import json
import sys

OS_NAME = sys.platform
HOME_PATH = Path.home()


def get_settings_path() -> str:
    """ Returns the settings dir path and creates it if it doesn't exist """

    if OS_NAME == "linux":
        settings_path = HOME_PATH / ".config" / "nunnix-manga"
    if OS_NAME == "win32":
        settings_path = HOME_PATH / "AppData" / "Local" / "nunnix-manga"

    if not settings_path.exists():
        settings_path.mkdir(parents=True)

    return str(settings_path)


def get_settings_file_path() -> str:
    """ Returns the settings file path and creates it if it doesn't exist """

    settings_path_file = Path(get_settings_path(), "settings.json")
    if not settings_path_file.exists():
        settings_path_file.touch()

    return str(settings_path_file)


def get_settings_file_content() -> dict:
    """ Returns the settings file content as a dict.
    If the file is empty, it returns an empty dict """

    settings_path_file = Path(get_settings_file_path())
    settings_path_file_text = settings_path_file.read_text()

    if settings_path_file_text == "":
        return {}
    else:
        return json.loads(settings_path_file_text)


def get_theme_file_path() -> str:
    """ Returns the theme file path and creates it if it doesn't exist """

    theme_path_file = Path(get_settings_path(), "theme.json")
    if not theme_path_file.exists():
        theme_path_file.touch()

    return str(theme_path_file)


def get_theme_file_content() -> str:
    """ Returns the theme file content as a dict.
    If the file is empty, it returns an empty dict """

    theme_path_file = Path(get_theme_file_path())
    theme_path_file_text = theme_path_file.read_text()

    if theme_path_file_text == "":
        return {}
    else:
        return json.loads(theme_path_file_text)

# TODO: Refactor all tests

import os
import re
import asyncio

from pathlib import Path
from importlib import import_module

import pytest_asyncio
import pytest
import aiohttp

from app.core import scrapers


# Get scrapers names
def scrapers_name():
    names = []
    for file in Path(scrapers.__path__[0]).glob("*.py"):
        names.append(os.path.splitext(os.path.basename(file))[0])
    return names


@pytest.mark.parametrize("name", scrapers_name())
class TestMangaSearch:
    """
    Class to test the manga search. This includes the following tests:
        - Test the url length
            - Value expected: String with length greater than 0
        - Test the title length
            - Value expected: String with length greater than 0
        - Test the cover length
            - Value expected: String with length greater than 0
    """
    def test_url_length(self, name, search_manga):
        for manga in search_manga[name]:
            assert len(manga["link"]) > 0, manga

    def test_title_length(self, name, search_manga):
        for manga in search_manga[name]:
            assert len(manga["title"]) > 0, manga

    def test_cover_length(self, name, search_manga):
        for manga in search_manga[name]:
            assert len(manga["cover"]) > 0, manga


@pytest.mark.parametrize("name", scrapers_name())
class TestMangaData:
    """
    Class to test the manga data. This includes the following tests:
        - Test the title
            - Value expected: String with length greater than 0
        - Test the author
            - Value expected: String or None, if string,
                              its length must be greater than 0
        - Test the description
            - Value expected: String or None, if string,
                              its length must be greater than 0
        - Test the cover: String with length greater than 0, and must be a
                          valid url
        - Test the genres:
            - Value expected: List with length greater or equal to 0
        - Test the status
            - Value expected: String or None, if string,
                              its length must be greater than 0
        - Test the chapters:
            - Dict with the following values to be tested:
                - Total:
                    - Value expected: Integer greater than 0
                - Chapters:
                    - List of dicts with the following values to be tested,
                      can be empty:
                        - Name:
                            - Value expected: String with length greater than 0
                        - Date:
                            - Value expected: List with the following indexes:
                                - 0: String, must be the day of the month
                                - 1: String, must be the month of the year
                                - 2: String, must be the year
                        - Link:
                            - Value expected: String with length greater than 0
                        - Scanlation:
                            - Value expected: String or None, if string,
                                              its length must be greater than 0
    """
    def test_title(self, name, manga_data):
        title = manga_data[name]["title"]
        assert len(title) > 0 and type(title) == str, title

    def test_author(self, name, manga_data):
        author = manga_data[name]["author"]
        if author is not None:
            assert len(author) > 0 and type(author) == str, author

    def test_description(self, name, manga_data):
        description = manga_data[name]["description"]
        if description is not None:
            assert len(description) > 0 and type(description) == str,\
                description

    def test_cover(self, name, manga_data):
        url_pattern = re.compile(r"^(?:http|ftp)s?://")
        cover = manga_data[name]["cover"]
        assert len(cover) > 0 and url_pattern.match(cover), cover

    def test_genres(self, name, manga_data):
        genres = manga_data[name]["genres"]
        assert len(genres) >= 0 and type(genres) == list, genres

    def test_status(self, name, manga_data):
        status = manga_data[name]["status"]
        if status is not None:
            assert len(status) > 0 and type(status) == str, status

    def test_chapters_total(self, name, manga_data):
        chapters_total = manga_data[name]["chapters_data"]["total"]
        assert chapters_total > 0 and type(chapters_total) == int,\
            chapters_total

    def test_chapters_name(self, name, manga_data):
        chapters = manga_data[name]["chapters_data"]["chapters"]
        for chapter in chapters:
            chapter_name = chapter["name"]
            assert len(chapter_name) > 0 and type(chapter_name) == str,\
                chapter_name

    def test_chapters_date(self, name, manga_data):
        chapters = manga_data[name]["chapters_data"]["chapters"]
        for chapter in chapters:
            chapter_date = chapter["date"]
            assert len(chapter_date) == 3 and type(chapter["date"]) == list,\
                chapter["date"]
            assert len(chapter_date[0]) > 0 and type(chapter_date[0]) == str,\
                chapter_date[0]
            assert len(chapter_date[1]) > 0 and type(chapter_date[1]) ==\
                str, chapter_date[1]
            assert len(chapter_date[2]) > 0 and type(chapter_date[2]) ==\
                str, chapter_date[2]

    def test_chapters_link(self, name, manga_data):
        chapters = manga_data[name]["chapters_data"]["chapters"]
        for chapter in chapters:
            chapter_link = chapter["link"]
            assert len(chapter_link) > 0 and type(chapter_link) == str,\
                chapter_link

    def test_chapters_scanlation(self, name, manga_data):
        chapters = manga_data[name]["chapters_data"]["chapters"]
        for chapter in chapters:
            chapter_scanlation = chapter["scanlation"]
            if chapter_scanlation is not None:
                assert len(chapter_scanlation) > 0 and\
                    type(chapter_scanlation) == str, chapter_scanlation


@pytest.mark.parametrize("name", scrapers_name())
class TestChapterImages:
    """
    Class to test the chapter images. This includes the following tests:
        - Test the number of images
            - Value expected: List with length greater than 0
        - Test the images
            - Value expected: List with strings with length greater than 0
    """
    def test_images_number(self, name, chapter_images):
        images = chapter_images[name]
        assert len(images) > 0 and type(images) == list, images

    def test_images(self, name, chapter_images):
        images = chapter_images[name]
        for image in images:
            assert len(image) > 0 and type(image) == str, image


@pytest.mark.parametrize("name", scrapers_name())
class TestAdvancedSearchControls:
    """
    Class to test the advanced search controls. This includes the following
    tests:
        - Test the length of the controls
            - Value expected: None or List with length greater than 0
    """
    def test_controls(self, name, advanced_search_controls):
        controls = advanced_search_controls[name]
        if controls is not None:
            assert len(controls) > 0 and type(controls) == list, controls


# Asyncio event loop fixture
@pytest_asyncio.fixture(scope="module")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Fixture to get the scrapers list
@pytest_asyncio.fixture(scope="module")
async def scrapers_dict():
    connector = aiohttp.TCPConnector(force_close=True)
    aiohttp_client = aiohttp.ClientSession(connector=connector)
    scrapers_dict = {}  # Dict of scrapers

    # Loop in the scrapers directory (app/core/scrapers) and get *.py files
    for file in Path(scrapers.__path__[0]).glob("*.py"):
        # Get the module name
        name = os.path.splitext(os.path.basename(file))[0]
        # Import the module
        module = import_module(f"{scrapers.__name__}.{name}")

        # Loop in the module attributes and get the scraper class
        for attr in dir(module):
            class_obj = getattr(module, attr)
            # Check if the class has the "get_manga_data" method
            if hasattr(class_obj, "get_manga_data"):
                scrapers_dict[name] = class_obj(aiohttp_client)

    return scrapers_dict


# Fixture to fetch search_manga() method
@pytest_asyncio.fixture(scope="module")
async def search_manga(scrapers_dict):
    searches = {}  # Dict of searches
    for name, scraper in scrapers_dict.items():
        # Set the scraper name as key, and the search_manga() result as value
        searches[name] = await scraper.search_manga()
    return searches


# Fixture to fetch manga_data() method
@pytest_asyncio.fixture(scope="module")
async def manga_data(scrapers_dict, search_manga):
    data = {}  # Dict of data
    for name, scraper in scrapers_dict.items():
        last_manga = search_manga[name][0]["link"]  # Get the first manga link
        # Set the scraper name as key, and the manga_data() result of the frist
        # search as value
        data[name] = await scraper.get_manga_data(last_manga)
    return data


# Fixture to fetch get_chapter_images() method
@pytest_asyncio.fixture(scope="module")
async def chapter_images(scrapers_dict, manga_data, search_manga):
    images = {}
    for name, scraper in scrapers_dict.items():
        chapters = manga_data[name]["chapters_data"]["chapters"]
        if len(chapters) > 0:
            first_chapter = manga_data[name]["chapters_data"]["chapters"][0]
        else:
            for manga in search_manga[name]:
                data = await scraper.get_manga_data(manga["link"])
                if len(data["chapters_data"]["chapters"]) > 0:
                    first_chapter = data["chapters_data"]["chapters"][0]
                    break
        images[name] = await scraper.get_chapter_images(first_chapter["link"])
    return images


# Fixture to fetch get_advanced_search_controls() method
@pytest_asyncio.fixture(scope="module")
def advanced_search_controls(scrapers_dict):
    controls = {}
    for name, scraper in scrapers_dict.items():
        controls[name] = scraper.get_advanced_search_controls()
    return controls
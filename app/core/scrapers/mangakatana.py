from datetime import datetime
from requests import Request, Session

import requests
import re

from bs4 import BeautifulSoup

from core.utils.logger import logger

BASE_URL = "https://mangakatana.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)',
    'Referer': "http://mangakatana.com/"}


def get_manga_data(url: str) -> dict:
    """ Get manga data.

    Parameters
    ----------
    uuid : str
        The manga URL.

    Returns
    -------
    dict
        Dictionary with all the manga data.

    Example
    -------
        >>> get_manga_data("http://mangakatana.com/manga/solo-leveling.21708")

    Dictionary content
    ------------------
    data = {
        "title": "Kumo desu ga, nani ka?",
        "author": "Miura Kentaro",
        "description": "Some description",
        "cover": "https://i3.mangakatana.com/token/3A32n%2Ag%3A9o%2Ab.jpg",
        "genres: ["Ecchi", "BL", "Zombies", "Yuri"],
        "status": "completed" | "ongoing" | "hiatus" | "cancelled",
        "chapters_data": {
            "total": "100",
            "chapters": {
                "0": {
                    "name": "Ch.1 - Chapter 1",
                    "date": "2020-01-01",
                    "link": "6310f6a1-17ee-4890-b837-2ec1b372905b",
                    "scanlation": "Band of the Hawks"
                }
            }
        }
    }
    """
    # TODO: Status code handler
    logger.debug(f"Requesting manga data at {url}")
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "lxml")

    # Collects all manga attributes.
    logger.debug("Getting manga title...")
    title = soup.find("h1", {"class": "heading"})
    title = title.text.strip()

    logger.debug("Getting manga description...")
    description = soup.find("div", {"class": "summary"})
    description = description.find("p").text.strip()

    logger.debug("Getting manga cover...")
    cover = soup.find("img", {"alt": "[Cover]"})
    cover = cover.get("src")

    logger.debug("Getting manga genres...")
    genres = soup.find("div", {"class": "genres"}).find_all("a")
    genres = [genre.text.strip() for genre in genres]

    logger.debug("Getting manga status...")
    status = soup.find("div", {"class": "status"})
    status = status.text.strip()

    logger.debug("Getting manga author...")
    author = soup.find("a", {"class": "author"})
    author = author.text.strip()

    logger.debug("Getting manga chapters...")
    total_chapters = soup.find("div", {"class": "uk-width-medium-1-4"})
    total_chapters = re.search(r"\d+", total_chapters.text).group()
    chapters_data = soup.find("div", {"class": "chapters"}).find_all("tr")
    chapters = {}

    # Here, we get all the chapters attributes
    for i, chapter in enumerate(chapters_data[::-1]):

        name = chapter.find("div", {"class": "chapter"}).find("a").text.strip()
        date = chapter.find("div", {"class": "update_time"}).text.strip()
        date = datetime.strptime(date, "%b-%d-%Y").strftime("%d-%m-%Y")
        link = chapter.find("div", {"class": "chapter"}).find("a").get("href")
        scanlation = None
        chapters[f"{i}"] = {
            "name": name,
            "date": date.split("-"),
            "link": link,
            "scanlation": None
        }

        logger.debug(f"Name: {name} | Date: {date} | Scanlation: {scanlation}")

    # Create dictionary with all the manga data.
    chapters_data = {"total": total_chapters, "chapters": chapters}
    data = {
        "title": title,
        "author": author,
        "description": description,
        "cover": cover,
        "genres": genres,
        "status": status,
        "chapters_data": chapters_data
    }

    logger.debug("Done. Returning data...\n")
    return data


def get_chapters_images(url: str) -> list:
    """ Get chapter images.

    Parameters
    ----------
    url : str
        The chapter URL.

    Returns
    -------
    list
        A list with all images links.

    Example
    -------
        >>> get_chapter_images("https://mangakatana.com/manga/baki/c50")
    """
    # TODO: Status code handler
    logger.debug(f"Requesting chapters data at {url}")
    response = requests.get(url, headers=HEADERS)

    images = re.findall(r"var ytaw=\[('.+'),\]", response.text)[0]
    images = images.replace("'", "").split(",")
    logger.debug("\n\nIMAGE: " + "\n\nIMAGE: ".join(images))

    logger.debug("\nDone. Returning data...\n")
    return images


def search_manga(
    title: str = None,
    author: str = None,
    order: str = "latest",
    include_mode: str = "and",
    status: str = None,
    chapters: int = 1,
    genres: list = [],
    exclude_genres: list = [],
    page: int = 1
) -> dict:
    """ Search manga, with advanced parameters.

    Parameters
    ----------
    title : str, optional
        Name of the title to search. To work, it must be the only parameter.

    author : str, optional
        Name of the author to search. To work, it must be the only parameter.

    order : str, optional
        Sort by different methods. Valid options:
        "az" (alphabetically), "numc" (number of chapters), "new", "latest".

    include_mode : str, optional
        Valid options: "and" (all selected genres)
        and "or" (any selected genre).

    status : str, optional
        Current manga status. Valid options:
        "0" (cancelled), "1" (ongoing), "2" (completed).

    chapters : string, optional
        Minimum chapters numbers.

    genres : list, optional
        Genres name.

    exclude_genres : list, optional
        Excludes genres name.

    page : int, optional
        The page number.


    Returns
    -------
    list
        Dictionary with all manga results.

    Example
    -------
        >>> search_manga(genres=["Ecchi", "Harem"], status="1")

    List of valid genres
    ----------------------
    "4-koma", "action", "adult", "adventure", "artbook", "award-winning",
    "yuri", "comedy", "cooking", "smut", "drama", "ecchi", "yaoi", "shota",
    "fantasy", "gender-bender", "gore", "harem", "historical", "horror",
    "isekai", "josei", "loli", "manhua", "manhwa", "martial-arts", "mecha",
    "medical", "webtoon", "doujinshi", "one-shot", "overpowered-mc",
    "psychological", "reincarnation", "romance", "school-life", "sci-fi",
    "seinen", "sexual-violence", "tragedy", "shoujo", "shoujo-ai", "shounen",
    "shounen-ai", "slice-of-life", "mystery", "sports", "super-power",
    "supernatural", "survival", "time-travel", "music".
    """
    # TODO: Status code handler
    data = []

    # If title is not none, search only the title.
    if title is not None:
        url = f"{BASE_URL}/page/{page}?search={title}"
    elif author is not None:
        url = f"{BASE_URL}/page/{page}?search={author}&search_by=author"
    else:
        url = f"{BASE_URL}/manga/page/{page}"

    # Parameters
    payload = {
        "filter": 1,
        "order": order,
        "include_mode": include_mode,
        "status": status,
        "chapters": chapters,
        "genres": "_".join(genres),
        "exclude_genres": "_".join(exclude_genres)
    }

    # Prepare requests
    session = Session()
    response = Request("GET", url, params=payload
                       if title is None and author is None else None)
    logger.debug(f"Requesting search at {response.prepare().url}")

    response = session.send(response.prepare())
    soup = BeautifulSoup(response.text, "lxml")

    # If there is only a single result
    if not soup.find(id="book_list"):
        logger.debug("Total results: 1\n")

        title = soup.find("h1", {"class": "heading"}).text.strip()
        cover = soup.find("img", {"alt": "[Cover]"}).get("src")
        link = soup.find("meta", {"property": "og:url"}).get("content")

        data.append(
            {
                "title": title,
                "link": link,
                "cover": cover
            }
        )
    else:
        results = soup.find(id="book_list").find_all("div", {"class": "item"})
        logger.debug(f"Total results: {len(results)}\n")

        for result in results:
            title = result.find("h3").find("a").text.strip()
            link = result.find("h3").find("a").get("href")
            cover = result.find("img", {"alt": "[Cover]"}).get("src")

            data.append(
                {
                    "title": title,
                    "link": link,
                    "cover": cover
                }
            )

    logger.debug("Done. Returning data...\n")
    return data

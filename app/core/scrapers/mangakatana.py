from datetime import datetime
import requests
import re

from bs4 import BeautifulSoup

from core.utils.logger import logger


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
        "cover": "https://uploads.mangadex.org/covers/MUUID/CUUID.jpg.512.jpg",
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
    title = soup.find("h1", {"class": "heading"})
    title = title.text.strip()

    description = soup.find("div", {"class": "summary"})
    description = description.find("p").text.strip()

    cover = soup.find("img", {"alt": "[Cover]"})
    cover = cover.get("src")

    genres = soup.find("div", {"class": "genres"}).find_all("a")
    genres = [genre.text.strip() for genre in genres]

    status = soup.find("div", {"class": "status"})
    status = status.text.strip()

    author = soup.find("a", {"class": "author"})
    author = author.text.strip()

    total_chapters = soup.find("div", {"class": "uk-width-medium-1-4"})
    total_chapters = re.search(r"\d+", total_chapters.text).group()
    chapters_data = soup.find("div", {"class": "chapters"}).find_all("tr")
    chapters = {}

    logger.debug("Collecting chapters data...\n")
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


print(get_manga_data("https://mangakatana.com/manga/time-roulette.25837"))

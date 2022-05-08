import time
import re
import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from ..utils.logger import logger


# Decorator to searcher exceptions
def searcher_exception_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        # No results found and end of results
        except AttributeError as e:
            exception_info = {"is_exception": True, "exception": {}}
            exception_info["exception"]["message"] = str(e)

            if "page" in kwargs and kwargs["page"] == 1:
                logger.error("No results found")
                exception_info["exception"]["type"] = "no_results"
            else:
                logger.warning("End of results")
                exception_info["exception"]["type"] = "end_of_results"
            logger.error(e)

            return exception_info

    return wrapper


class Mangakatana:
    def __init__(self, session: ClientSession):
        self.session = session

        self.NAME = "MangaKatana"

        self.BASE_URL = "https://mangakatana.com"
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)',
            'Referer': "http://mangakatana.com/"}
        self.MONTHS = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12"
        }

    async def get_manga_data(self, url: str) -> dict:
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
            >>> get_manga_data("http://mangakatana.com/manga/solo-leveling")

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
                "total": 100,
                "chapters": [
                    {
                        "name": "Ch.1 - Chapter 1",
                        "date": "2020-01-01",
                        "link": "6310f6a1-17ee-4890-b837-2ec1b372905b",
                        "scanlation": "Band of the Hawks"
                    }
                ]
            }
        }
        """
        # TODO: Status code handler
        # Prepare requests
        logger.debug("Requesting manga data...")
        async with self.session.get(url, headers=self.HEADERS) as response:
            logger.debug(f"Requested manga data at {response.url}")
            soup = BeautifulSoup(await response.text(), "lxml")

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
        total_chapters = int(re.search(r"\d+", total_chapters.text).group())
        chapters_data = soup.find("div", {"class": "chapters"}).find_all("tr")
        chapters = []

        # Here, we get all the chapters attributes
        for chapter in chapters_data[::-1]:

            name = chapter.find("div", {"class": "chapter"}).find("a")
            name = name.text.strip()

            # Replace the month name with the corresponding number
            date = chapter.find("div", {"class": "update_time"}).text.strip()
            date = [date.replace(m, self.MONTHS[m]) for m in self.MONTHS
                    if m in date][0]
            date = time.strptime(date, "%m-%d-%Y")
            date = time.strftime("%d-%m-%Y", date)

            link = chapter.find("div", {"class": "chapter"}).find("a")
            link = link.get("href")
            scanlation = None
            chapters.append({
                "name": name,
                "date": date.split("-"),
                "link": link,
                "scanlation": None
            })

            logger.debug(f"Name: {name}|Date:{date}|Scanlation: {scanlation}")

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

    async def get_chapter_images(self, url: str) -> list:
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
        # Prepare requests
        logger.debug("Requesting chapters data...")
        async with self.session.get(url, headers=self.HEADERS) as response:
            logger.debug(f"Requested chapters data at {response.url}")
            images = re.findall(r"var ytaw=\[('.+'),\]", await response.text())

        images = images[0].replace("'", "").split(",")
        logger.debug("\n\nIMAGE: " + "\n\nIMAGE: ".join(images))

        logger.debug("\nDone. Returning data...\n")
        return images

    @searcher_exception_handler
    async def search_manga(
        self,
        title: str = "",
        author: str = "",
        order: str = "latest",
        include_mode: str = "and",
        status: str = None,
        chapters: int = 1,
        include_genres: list = [],
        exclude_genres: list = [],
        page: int = 1
    ) -> dict:
        """ Search manga, with advanced parameters.

        Parameters
        ----------
        title : str, optional
            Name of the title to search. To work, it must be the only parameter

        author : str, optional
            Name of the author. To work, it must be the only parameter

        order : str, optional
            Sort by different methods. Valid options:
            "az" (alphabetically), "numc" (number of chapters), "new", "latest"

        include_mode : str, optional
            Valid options: "and" (all selected genres)
            and "or" (any selected genre).

        status : str, optional
            Current manga status. Valid options:
            "0" (cancelled), "1" (ongoing), "2" (completed).

        chapters : string, optional
            Minimum chapters numbers.

        include_genres : list, optional
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
        "seinen", "sexual-violence", "tragedy", "shoujo", "shoujo-ai",
        "shounen-ai", "slice-of-life", "mystery", "sports", "super-power",
        "supernatural", "survival", "time-travel", "music", "shounen".
        """
        # TODO: Status code handler
        data = []

        # If title is not none, search only the title.
        if title != "":
            url = f"{self.BASE_URL}/page/{page}?search={title}"
        elif author != "":
            url = f"{self.BASE_URL}/page/{page}?search={author}"
            url += "&search_by=author"
        else:
            url = f"{self.BASE_URL}/manga/page/{page}"

        # Parameters
        payload = {
            "filter": 1,
            "order": order,
            "include_mode": include_mode,
            "status": status,
            "chapters": chapters,
            "include": "_".join(include_genres),
            "exclude": "_".join(exclude_genres)
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        # Prepare requests
        logger.debug("Requesting search...")
        async with self.session.get(url, params=payload
                                    if title == "" and author == "" else None,
                                    headers=self.HEADERS) as response:
            logger.debug(f"Requested search at {response.url}")

            # Run in a separate thread to avoid being blocked by bs4
            loop = asyncio.get_event_loop()
            soup = await loop.run_in_executor(None, BeautifulSoup,
                                              await response.text(), "lxml")

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
            results = soup.find(id="book_list")
            results = results.find_all("div", {"class": "item"})
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

    def get_advanced_search_controls(self) -> dict | None:
        """ Return advanced search controls.

        Returns
        -------
        dict
            Dictionary with all advanced search controls.
        """

        label_1 = {
            "type": "label",
            "content": "NOTE: Title and author are mutually exclusive!",
            "bold": True,
        }
        title = {
            "name": "Title",
            "type": "textfield",
            "parameter": "title",
        }
        author = {
            "name": "Author",
            "type": "textfield",
            "parameter": "author",
        }
        label_2 = {
            "type": "label",
            "content": ("NOTE: These sections will be ignored if the title " +
                        "and author are not empty."),
            "bold": True,
            "topPadding": 20,
        }
        order = {
            "name": "Sort by",
            "type": "combobox",
            "parameter": "order",
            "content": [
                {"name": "Latest update", "parameter": "latest"},
                {"name": "New manga", "parameter": "new"},
                {"name": "Alphabetically", "parameter": "az"},
                {"name": "Number of chapters", "parameter": "numc"}
            ],
        }
        include_mode = {
            "name": "Genre Inclusion mode:",
            "type": "combobox",
            "parameter": "include_mode",
            "content": [
                {"name": "AND (All Selected Genres)", "parameter": "and"},
                {"name": "OR (Any Selected Genres)", "parameter": "or"}
            ]
        }
        status = {
            "name": "Status",
            "type": "combobox",
            "parameter": "status",
            "content": [
                {"name": "See all", "parameter": None},
                {"name": "Ongoing", "parameter": 1},
                {"name": "Completed", "parameter": 2},
                {"name": "Cancelled", "parameter": 0}
            ]
        }
        chapters = {
            "name": "Minimum chapters",
            "type": "slider",
            "parameter": "chapters",
            "from": 0,
            "to": 500,
            "stepSize": 20,
        }
        genres = {
            "name": "Genres",
            "type": "tristate-checkbox",
            "checked_parameter": "include_genres",
            "unchecked_parameter": "exclude_genres",
            "content": [
                {"name": "4-Koma", "parameter": "4-koma"},
                {"name": "Action", "parameter": "action"},
                {"name": "Adult", "parameter": "adult"},
                {"name": "Adventure", "parameter": "adventure"},
                {"name": "Artbook", "parameter": "artbook"},
                {"name": "Award-winning", "parameter": "award-winning"},
                {"name": "Yuri", "parameter": "yuri"},
                {"name": "Comedy", "parameter": "comedy"},
                {"name": "Cooking", "parameter": "cooking"},
                {"name": "Doujinshi", "parameter": "doujinshi"},
                {"name": "Drama", "parameter": "drama"},
                {"name": "Ecchi", "parameter": "ecchi"},
                {"name": "Fantasy", "parameter": "fantasy"},
                {"name": "Gender bender", "parameter": "gender-bender"},
                {"name": "Gore", "parameter": "gore"},
                {"name": "Harem", "parameter": "harem"},
                {"name": "Historical", "parameter": "historical"},
                {"name": "Horror", "parameter": "horror"},
                {"name": "Isekai", "parameter": "isekai"},
                {"name": "Josei", "parameter": "josei"},
                {"name": "Loli", "parameter": "loli"},
                {"name": "Manhua", "parameter": "manhua"},
                {"name": "Manhwa", "parameter": "manhwa"},
                {"name": "Martial arts", "parameter": "martial-arts"},
                {"name": "Mecha", "parameter": "mecha"},
                {"name": "Medical", "parameter": "medical"},
                {"name": "Webtoon", "parameter": "webtoon"},
                {"name": "Doujinshi", "parameter": "doujinshi"},
                {"name": "One shot", "parameter": "one-shot"},
                {"name": "Overpowered mc", "parameter": "overpowered-mc"},
                {"name": "Psychological", "parameter": "psychological"},
                {"name": "Reincarnation", "parameter": "reincarnation"},
                {"name": "Romance", "parameter": "romance"},
                {"name": "School life", "parameter": "school-life"},
                {"name": "Sci fi", "parameter": "sci-fi"},
                {"name": "Seinen", "parameter": "seinen"},
                {"name": "Sexual violence", "parameter": "sexual-violence"},
                {"name": "Tragedy", "parameter": "tragedy"},
                {"name": "Shoujo", "parameter": "shoujo"},
                {"name": "Shoujo ai", "parameter": "shoujo-ai"},
                {"name": "Shounen", "parameter": "shounen"},
                {"name": "Shounen ai", "parameter": "shounen-ai"},
                {"name": "Slice of life", "parameter": "slice-of-life"},
                {"name": "Mystery", "parameter": "mystery"},
                {"name": "Sports", "parameter": "sports"},
                {"name": "Super power", "parameter": "super-power"},
                {"name": "Supernatural", "parameter": "supernatural"},
                {"name": "Survival", "parameter": "survival"},
                {"name": "Time travel", "parameter": "time-travel"},
                {"name": "Music", "parameter": "music"}
            ],
        }

        return [label_1, title, author, label_2, order, include_mode, status,
                chapters, genres]

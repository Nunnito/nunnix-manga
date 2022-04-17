from requests import Request, Session
import requests
import re

from core.utils.logger import logger


LANG = "en"  # Used to get manga by language
QUALITY_MODE = "data"  # Image quality mode: "data" or "data-saver"
BASE_URL = "https://api.mangadex.org"  # Used for API requests


def get_manga_data(uuid: str) -> dict:
    """ Get manga data.

    Parameters
    ----------
    uuid : str
        The manga UUID.

    Returns
    -------
    dict
        Dictionary with all the manga data.

    Example
    -------
        >>> get_manga_data("801513ba-a712-498c-8f57-cae55b38cc92")

    Dictionary content
    ------------------
    data = {
        "title": "",
        "author": "",
        "description": "",
        "cover": "",
        "genres: [],
        "status": "",
        "chapters_data": ""
    }
    """
    # TODO: Status code handler
    logger.info("Getting manga data...")
    api_manga = f"{BASE_URL}/manga/{uuid}"

    logger.debug(f"Requesting manga data at {api_manga}")
    response = requests.get(api_manga)

    attrs = response.json()["data"]["attributes"]
    relationships = response.json()["data"]["relationships"]

    # Collects all manga attributes.
    logger.debug("Getting manga title...")
    title = attrs["title"][LANG]

    logger.debug("Getting manga description...")
    description = attrs["description"]

    logger.debug("Getting manga cover...")
    cover_id = [i for i in relationships if i["type"] == "cover_art"][0]["id"]
    cover = get_manga_cover(cover_id, 512)[uuid]

    logger.debug("Getting manga cover...")
    genres = [genre["attributes"]["name"][LANG] for genre in attrs["tags"]]

    logger.debug("Getting manga status...")
    status = attrs["status"]

    author = get_manga_author(relationships[0]["id"])
    chapters_data = get_chapters_data(uuid)

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
    logger.info("Done!\n")
    return data


def get_manga_author(uuid: str) -> str:
    """ Get manga author. This function is used by get_manga_data function.

    Parameters
    ----------
    uuid : str
        The author UUID.

    Returns
    -------
    str
        Author name.
    """
    # TODO: Status code handler
    api_author = f"{BASE_URL}/author/{uuid}"

    logger.debug(f"Requesting author data at {api_author}")
    response = requests.get(api_author)

    logger.debug("Getting manga author...")
    attrs = response.json()["data"]["attributes"]
    author = attrs["name"]

    logger.debug("Done. Returning data...")
    return author


def get_chapters_data(uuid: str, offset: int = 0) -> dict:
    """ Get chapters data. This function is used by get_manga_data function.

    Parameters
    ----------
    uuid : str
        The manga UUID.
    offset : int (optional)
        The offset to get the chapters.

    Returns
    -------
    dict
        Dictionary with all chapters data.
    """
    # TODO: Status code handler
    api_chapters_data = (f"{BASE_URL}/manga/{uuid}/feed?limit=500&" +
                         f"offset={offset}&order[chapter]=asc&" +
                         f"translatedLanguage[]={LANG}")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")

    chapters = {}
    scanlations = {}
    users = {}

    logger.debug(f"Requesting chapters data at {api_chapters_data}")
    response = requests.get(api_chapters_data)

    total = response.json()["total"]
    results = response.json()["data"]

    logger.debug("Collecting chapters data...\n")

    # Iterate through results, and append scanlations to the list.
    for result in results:
        relationships = result["relationships"]
        scanlations[result["id"]] = []

        for relationship in relationships:
            if relationship["type"] == "scanlation_group":
                scanlations[result["id"]].append(relationship["id"])
            elif relationship["type"] == "user":
                if not scanlations[result["id"]]:
                    users[result["id"]] = relationship["id"]

    users = get_chapter_user(users)
    scanlations = get_chapter_scanlation(scanlations)
    scanlations.update(users)

    # Here, we get all the attributes
    for i, result in enumerate(results, offset):
        attrs = result["attributes"]

        name = f"Ch.{attrs['chapter']} - {attrs['title']}"
        date = re.match(date_pattern, attrs["publishAt"]).group()
        scanlation = scanlations[result["id"]]
        chapter_id = result["id"]
        chapters[f"{i}"] = {
            "name": name,
            "date": date,
            "link": chapter_id,
            "scanlation": scanlations[chapter_id]
            }

        logger.debug(f"Name: {name} | Date: {date} | Scanlation: {scanlation}")

    data = {"total": total, "chapters": chapters}

    if total > 500 and offset + 500 < total:
        data["chapters"].update(get_chapters_data(uuid,
                                                  offset + 500)["chapters"])

    logger.debug(f"Done. Returning data... (offset: {offset})")
    return data


def get_chapter_scanlation(scanlations_dict: dict[str: str]) -> str:
    """ Get chapters scanlations. This function is used by get_chapter_data.

    Parameters
    ----------
    uuid : dict[str: str]
        Scanlations dict with chapter UUID as key.

    Returns
    -------
    str
        Scanlation data.
    """
    # TODO: Status code handler

    # Get scanlations UUIDs, and remove duplicates
    uuid = []
    for scanlations_id in scanlations_dict.values():
        for scanlation_id in scanlations_id:
            uuid.append(scanlation_id)

    uuid = list(set(uuid))

    scanlation = {}  # Scanlations dict
    data = {}  # Scanlations data
    payload = {"ids[]": uuid, "limit": 100}

    # Prepare requests
    session = Session()
    response = Request("GET", BASE_URL + "/group", params=payload).prepare()
    logger.debug(f"Requesting scanlations at {response.url}")

    response = session.send(response)  # Make request
    results = response.json()["data"]

    # Iterate through results, and append the scanlation name to the dict.
    for result in results:
        scanlation_id = result["id"]
        attributes = result["attributes"]
        name = attributes["name"]

        scanlation[scanlation_id] = name

    # Iterate through scanlations dict, and set the scanlation name to the
    # chapter UUID.
    for chapter_id, scanlation_ids in scanlations_dict.items():
        data[chapter_id] = []
        # Iterate through scanlations UUIDs, and append the scanlation name
        for scanlation_id in scanlation_ids:
            data[chapter_id].append(scanlation[scanlation_id])

        data[chapter_id] = " | ".join(data[chapter_id])

    logger.debug("Done. Returning data...\n")
    return data


def get_chapter_user(users_dict: dict[str: str]) -> str:
    """ Get chapters users. This function is used by get_chapter_data.

    Parameters
    ----------
    uuid : dict[str: str]
        Users dict with chapter UUID as key.

    Returns
    -------
    str
        Users data.
    """
    # TODO: Status code handler

    # Get users UUIDs, and remove duplicates
    uuid = list(set(users_dict.values()))

    user = {}  # Users dict
    data = {}  # Users data

    for user_id in uuid:
        # Prepare requests
        session = Session()
        response = Request("GET", BASE_URL + "/user/" + user_id).prepare()
        logger.debug(f"Requesting users at {response.url}")

        response = session.send(response)  # Make request
        result = response.json()["data"]

        # Append the user name to the dict.
        user_id = result["id"]
        name = result["attributes"]["username"]
        user[user_id] = name

    # Iterate through users dict, and set the user name to the
    # chapter UUID.
    for chapter_id, user_id in users_dict.items():
        data[chapter_id] = user[user_id]

    logger.debug("Done. Returning data...\n")
    return data


def get_chapter_images(uuid: str) -> list:
    """ Get chapter images.

    Parameters
    ----------
    uuid : str
        The chapter UUID.

    Returns
    -------
    list
        A list with all images links.

    Example
    -------
        >>> get_chapter_images("da63389a-3d60-4634-8652-47a52e35eacc")
    """
    # TODO: Status code handler

    logger.info("Getting chapters images...")

    api_at_home = f"{BASE_URL}/at-home/server/{uuid}"
    api_chapter_images = f"{BASE_URL}/chapter/{uuid}"
    images = []

    # Requests
    logger.debug(f"Requesting base url at {api_at_home}")
    base_url = requests.get(api_at_home).json()["baseUrl"]
    logger.debug(f"Requesting chapter data at {api_chapter_images}")
    data = requests.get(api_chapter_images).json()
    attributes = data["data"]["attributes"]

    # Necessary data to make URLs
    logger.debug("Getting chapter hash...")
    hash = attributes["hash"]
    logger.debug("Getting chapter images name...")
    logger.debug(f"Quality mode is \"{QUALITY_MODE}\"")
    names = attributes["data" if QUALITY_MODE == "data" else "dataSaver"]

    # Making images URLs
    logger.debug("Making images URLs...\n")
    for i, name in enumerate(names):
        image_url = f"{base_url}/{QUALITY_MODE}/{hash}/{name}"
        images.append(image_url)
        logger.debug(f"IMAGE {i}: {image_url}\n")

    logger.debug("Done. Returning data...")
    logger.info("Done!")

    return images


def search_manga(
    limit: int = 25,
    offset: int = None,
    title: str = None,
    authors: list[str] = None,
    artists: list[str] = None,
    year: int = None,
    include_tags: list[str] = None,
    included_tags_mode: str = None,
    excluded_tags: list[str] = None,
    excluded_tags_mode: str = None,
    status: list[str] = None,
    original_language: list[str] = None,
    publication_demographic: list[str] = None,
    ids: list[str] = None,
    content_rating: list[str] = None,
    created_at_since: str = None,
    updated_at_since: str = None,
    order: dict[str, str] = None,
) -> dict:
    """ Search manga, with advanced parameters.
        See: https://api.mangadex.org/docs.html#operation/get-search-manga

    Parameters
    ----------
    limit : int, optional
        Number of results
    offset : int, optional
        Offset between mangas, this will be used to "jump" to the next page.
    title : str, optional
        Manga title.
    authors : list[str], optional
        Manga authors (UUID).
    artists : list[str], optional
        Manga artist (UUID).
    year : int, optional
        Manga year.
    include_tags : list[str], optional
        Manga genres (UUID).
    included_tags_mode : str, optional
        Genres inclusion mode ("AND" or "OR").
    excluded_tags : list[str], optional
        Manga excluded genres.
    excluded_tags_mode : str, optional
        Excluded genres inclusion mode ("AND" or "OR")
    status : list[str], optional
        Manga status ("ongoing", "completed", "hiatus", "cancelled").
    original_language : list[str], optional
        Manga original language, in ISO 639-1 standard.
    publication_demographic : list[str], optional
        Manga demography ("shounen", "shoujo", "josei", "seinen", "none").
    ids : list[str], optional
        Manga ids (UUID).
    content_rating : list[str], optional
        Manga content rating ("none", "safe", "suggestive", "erotica",
        "pornographic").
    created_at_since : str, optional
        Datetime string with following format: YYYY-MM-DDTHH:MM:SS
    updated_at_since : str, optional
        Datetime string with following format: YYYY-MM-DDTHH:MM:SS
    order : dict[str, str], optional
        Manga order (createdAt: "asc", "desc". updatedAt: "asc", "desc").

    Returns
    -------
    dict
        Dictionary with all manga results.

    Example
    -------
        >>> search_manga(title="Kumo", offset=20, order={"updatedAt": "asc"})
    """
    # TODO: Status code handler

    # Query strings
    payload = {
        "limit": limit,
        "offset": offset,
        "title": title,
        "authors": authors,
        "artists": artists,
        "year": year,
        "includeTags": include_tags,
        "includedTagsMode": included_tags_mode,
        "excludedTags": excluded_tags,
        "excludedTagsMode": excluded_tags_mode,
        "status": status,
        "originalLanguage": original_language,
        "publicationDemographic": publication_demographic,
        "ids": ids,
        "contentRating": content_rating,
        "createdAtSince": created_at_since,
        "updatedAtSince": updated_at_since,
        ("order" if order is None else f"order[{list(order.keys())[0]}]"):
        (order if order is None else order[list(order.keys())[0]])
    }

    data = []  # To store searches

    # Prepare requests
    session = Session()
    response = Request("GET", BASE_URL + "/manga", params=payload).prepare()
    logger.info("Searching manga...")
    logger.debug(f"Requesting search at {response.url}")

    response = session.send(response)  # Make request
    results = response.json()["data"]

    logger.debug(f"Total results: {response.json()['total']}\n")

    for result in results:
        attributes = result["attributes"]
        relationships = result["relationships"]

        title = attributes["title"]["en"]
        link = result["id"]
        cover = [i for i in relationships if i["type"] == "cover_art"][0]["id"]

        logger.debug(f"Title {title}")
        logger.debug(f"Link {link}")
        logger.debug(f"Cover {cover}\n")

        data.append({
            "title": title,
            "link": link,
            "cover": cover
        })

    # Replace covers UUID with covers URL.
    c_list = [cover["cover"] for cover in data]
    c_dict = get_manga_cover(c_list)

    for i in range(len(data)):
        data[i]["cover"] = c_dict[data[i]["link"]]

    logger.debug("Done. Returning data...")
    logger.info("Done!")
    return data


def get_manga_cover(uuid: list[str], resolution: int = 256) -> dict[str, str]:
    """ Get manga covers by UUID.

    Parameters
    ----------
    uuid : list[str]
        Covers UUID

    Returns
    -------
    dict[str, str]
        Covers URL
    """
    # TODO: Status code handler

    covers = {}  # Covers dict
    payload = {"ids[]": uuid, "limit": 25}

    # Prepare requests
    session = Session()
    response = Request("GET", BASE_URL + "/cover", params=payload).prepare()
    logger.debug(f"Requesting covers at {response.url}")

    response = session.send(response)  # Make request
    results = response.json()["data"]

    # Iterate through resutls, and append the cover URL to the dict.
    for result in results:
        attributes = result["attributes"]
        manga = result["relationships"][0]["id"]
        name = attributes["fileName"]
        cover = (f"https://uploads.mangadex.org/covers/{manga}/{name}" +
                 f".{resolution}.jpg")

        covers[manga] = cover

    logger.debug("Done. Returning data...\n")
    return covers

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
    relationships = response.json()["relationships"]

    # Collects all manga attributes.
    logger.debug("Getting manga title...")
    title = attrs["title"][LANG]
    logger.debug("Getting manga description...")
    description = attrs["description"]
    logger.debug("Getting manga cover...")
    cover = relationships[-1]["id"]
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


def get_chapters_data(uuid: str) -> dict:
    """ Get chapters data. This function is used by get_manga_data function.

    Parameters
    ----------
    uuid : str
        The manga UUID.

    Returns
    -------
    dict
        Dictionary with all chapters data.
    """
    # TODO: Status code handler
    api_chapters_data = (f"{BASE_URL}/manga/{uuid}/feed?limit=500&" +
                         f"order[chapter]=asc&translatedLanguage[]={LANG}")
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")

    chapters = {}

    logger.debug(f"Requesting chapters data at {api_chapters_data}")
    response = requests.get(api_chapters_data)

    total = response.json()["total"]
    results = response.json()["results"]

    logger.debug("Collecting chapters data...\n")
    # Here, we get all the attributes
    for i, result in enumerate(results):
        results_data = result["data"]
        attrs = results_data["attributes"]

        name = attrs["chapter"] + " " + attrs["title"]
        date = re.match(date_pattern, attrs["publishAt"]).group()
        chapter_id = results_data["id"]
        chapters[f"{i}"] = {"name": name, "date": date, "link": chapter_id}

        logger.debug(f"Name: {name} | Date: {date} | UUID: {chapter_id}\n")

    data = {"total": total, "chapters": chapters}

    logger.debug("Done. Returning data...")
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
    results = response.json()["results"]

    logger.debug(f"Total results: {response.json()['total']}\n")

    for result in results:
        attributes = result["data"]["attributes"]
        relationships = result["relationships"]

        title = attributes["title"]["en"]
        link = result["data"]["id"]
        cover = relationships[-1]["id"]

        logger.debug(f"Title {title}")
        logger.debug(f"Link {link}")
        logger.debug(f"Cover {cover}\n")

        data.append({
            "title": title,
            "link": link,
            "cover": cover
        })

    logger.debug("Done. Returning data...")
    logger.info("Done!")
    return data


def get_manga_cover(m_uuid: str, c_uuid: str) -> str:
    # Prepare requests
    session = Session()
    response = Request("GET", BASE_URL + f"/cover/{c_uuid}").prepare()
    logger.debug(f"Requesting cover at {response.url}")

    response = session.send(response)  # Make request
    attributes = response.json()["data"]["attributes"]
    filename = attributes["fileName"]
    cover = f"https://uploads.mangadex.org/covers/{m_uuid}/{filename}.256.jpg"

    logger.debug("Done. Returning data...\n")
    return cover

# search = search_manga(title="Berserk")
data = get_manga_data("801513ba-a712-498c-8f57-cae55b38cc92")

print(data)

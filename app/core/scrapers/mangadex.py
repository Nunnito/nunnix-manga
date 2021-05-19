import requests
import re

LANG = "en"  # Used to get manga by language


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
        "total_chapters": ""
    }
    """
    # TODO: Status code handler

    response = requests.get(f"https://api.mangadex.org/manga/{uuid}")

    attrs = response.json()["data"]["attributes"]
    relationships = response.json()["relationships"]

    # Gathers all manga attributes.
    title = attrs["title"][LANG]
    author = get_manga_author(relationships[0]["id"])
    description = attrs["description"]
    cover = "https://i.imgur.com/BY58k5E.jpg"
    genres = [genre["attributes"]["name"][LANG] for genre in attrs["tags"]]
    status = attrs["status"]
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

    response = requests.get(f"https://api.mangadex.org/author/{uuid}")

    attrs = response.json()["data"]["attributes"]
    author = attrs["name"]

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

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")

    chapters = {}
    response = requests.get(f"https://api.mangadex.org/manga/{uuid}/feed?\
                              limit=500&order[chapter]=asc&locales[]={LANG}")

    total = response.json()["total"]
    results = response.json()["results"]

    # Here, we get all the attributes
    for i, result in enumerate(results):
        results_data = result["data"]
        attrs = results_data["attributes"]

        name = attrs["chapter"] + " " + attrs["title"]
        date = re.match(date_pattern, attrs["publishAt"]).group()
        chapter_id = results_data["id"]
        chapters[f"{i}"] = {"name": name, "date": date, "link": chapter_id}

    data = {"total": total, "chapters": chapters}

    return data

import time
import re

from aiohttp import ClientSession

from ...utils.logger import logger


# Decorator to searcher exceptions
def searcher_exception_handler(func):
    async def wrapper(*args, **kwargs):
        results = await func(*args, **kwargs)

        # No results found and end of results
        if results == []:
            results = {"is_exception": True, "exception": {}}
            results["exception"]["message"] = "n/a"

            if "page" in kwargs and kwargs["page"] == 1:
                logger.error("No results found")
                results["exception"]["type"] = "no_results"
            else:
                logger.warning("End of results")
                results["exception"]["type"] = "end_of_results"

        return results

    return wrapper


class Mangadex:
    NAME = "MangaDex"  # Used for GUI
    TYPE = "manga"

    def __init__(self, session: ClientSession):
        self.session = session  # Aiohttp session

        self.LANG = "en"  # Used to get manga by language
        self.QUALITY_MODE = "data"  # Image quality: "data" or "data-saver"
        self.BASE_URL = "https://api.mangadex.org"  # Used for API requests
        self.COVERS_URL = "https://uploads.mangadex.org/covers"
        self.TAGS = {  # Genres UUIDs. Thanks MangaDexFilters.kt
            0: "391b0423-d847-456f-aff0-8b0cfc03066b",
            1: "f4122d1c-3b44-44d0-9936-ff7502c39ad3",
            2: "87cc87cd-a395-47af-b27a-93258283bbc6",
            3: "e64f6742-c834-471d-8d72-dd51fc02b835",
            4: "3de8c75d-8ee3-48ff-98ee-e20a65c86451",
            5: "51d83883-4103-437c-b4b1-731cb73d786c",
            6: "0a39b5a1-b235-4886-a747-1d05d216532d",
            7: "5920b825-4181-4a17-beeb-9918b0ff7a30",
            8: "4d32cc48-9f00-4cca-9b5a-a839f0764984",
            9: "ea2bc92d-1c26-4930-9b7c-d5c0dc1b6869",
            10: "5ca48985-9a9d-4bd8-be29-80dc0303db72",
            11: "9ab53f92-3eed-4e9b-903a-917c86035ee3",
            12: "da2d50ca-3018-4cc0-ac7a-6b7d472a29ea",
            13: "39730448-9a5f-48a2-85b0-a70db87b1233",
            14: "b13b2a48-c720-44a9-9c77-39c9979373fb",
            15: "b9af3a63-f058-46de-a9a0-e0c13906197a",
            16: "7b2ce280-79ef-4c09-9b58-12b7c23a9b78",
            17: "cdc58593-87dd-415e-bbc0-2ec27bf404cc",
            18: "b11fda93-8f1d-4bef-b2ed-8803d3733170",
            19: "f5ba408b-0e7a-484d-8d49-4e9125ac96de",
            20: "2bd2e8d0-f146-434a-9b51-fc9ff2c5fe6a",
            21: "3bb26d85-09d5-4d2e-880c-c34b974339e9",
            22: "a3c67850-4684-404e-9b7f-c69850ee5da6",
            23: "b29d6a3d-1569-4e7a-8caf-7557bc92cd5d",
            24: "fad12b5e-68ba-460e-b933-9ae8318f5b65",
            25: "aafb99c1-7f60-43fa-b75f-fc9502ce29c7",
            26: "33771934-028e-4cb3-8744-691e866a923e",
            27: "cdad7e68-1419-41dd-bdce-27753074a640",
            28: "5bd0e105-4481-44ca-b6e7-7544da56b1a3",
            29: "ace04997-f6bd-436e-b261-779182193d3d",
            30: "2d1f5d56-a1e5-4d0d-a961-2193588b08ec",
            31: "3e2b8dae-350e-4ab8-a8ce-016e844b9f0d",
            32: "85daba54-a71c-4554-8a28-9901a8b0afad",
            33: "a1f53773-c69a-4ce5-8cab-fffcd90b1565",
            34: "81c836c9-914a-4eca-981a-560dad663e73",
            35: "799c202e-7daa-44eb-9cf7-8a3c0441531e",
            36: "50880a9d-5440-4732-9afb-8f457127e836",
            37: "c8cbe35b-1b2b-4a3f-9c37-db84c4514856",
            38: "ac72833b-c4e9-4878-b9db-6c8a4a99444a",
            39: "dd1f77c5-dea9-4e2b-97ae-224af09caf99",
            40: "36fd93ea-e8b8-445e-b836-358f02b3d33d",
            41: "f42fbf9e-188a-447b-9fdc-f19dc1e4d685",
            42: "ee968100-4191-4968-93d3-f82d72be7e46",
            43: "489dd859-9b61-4c37-af75-5b18e88daafc",
            44: "92d6d951-ca5e-429c-ac78-451071cbf064",
            45: "320831a8-4026-470b-94f6-8353740e6f04",
            46: "0234a31e-a729-4e28-9d6a-3f87c4966b9e",
            47: "b1e97889-25b4-4258-b28b-cd7f4d28ea9b",
            48: "df33b754-73a3-4c54-80e6-1a74a8058539",
            49: "9467335a-1b83-4497-9231-765337a00b96",
            50: "3b60b75c-a2d7-4860-ab56-05f391bb889c",
            51: "0bc90acb-ccc1-44ca-a34a-b9f3a73259d0",
            52: "65761a2a-415e-47f3-bef2-a9dababba7a6",
            53: "423e2eae-a7a2-4a8b-ac03-a8351462d71d",
            54: "81183756-1453-4c81-aa9e-f6e1b63be016",
            55: "caaa44eb-cd40-4177-b930-79d3ef2afe87",
            56: "256c8bd9-4904-4360-bf4f-508a76d67183",
            57: "97893a4c-12af-4dac-b6be-0dffb353568e",
            58: "ddefd648-5140-4e5f-ba18-4eca4071d19b",
            59: "e5301a23-ebd9-49dd-a0cb-2add944c7fe9",
            60: "69964a64-2f90-4d33-beeb-f3ed2875eb4c",
            61: "7064a261-a137-4d3a-8848-2d385de3a99c",
            62: "eabc5b4c-6aff-42f3-b657-3e90cbd00b75",
            63: "5fff9cde-849c-4d78-aab0-0d52b2ee1d25",
            64: "07251805-a27e-4d59-b488-f0bfbec15168",
            65: "292e862b-2d17-4062-90a2-0356caa4ae27",
            66: "f8f62932-27da-4fe4-8ee1-6779a8c5edba",
            67: "31932a7e-5b8e-49a6-9f12-2afa39dc544c",
            68: "891cf039-b895-47f0-9229-bef4c96eccd4",
            69: "d7d1730f-6eb0-4ba6-9437-602cac38664c",
            70: "9438db5a-7e2a-4ac0-b39e-e0d95a34b8a8",
            71: "d14322ac-4d6f-4e9b-afd9-629d5f4d8a41",
            72: "8c86611e-fab7-4986-9dec-d1a2f44acdd5",
            73: "e197df38-d0e7-43b5-9b09-2842d0c326dd",
            74: "acc803a4-c95a-4c22-86fc-eb6b582d82a2",
            75: "631ef465-9aba-4afb-b0fc-ea10efe274a8"
        }

    async def get_content_data(self, uuid: str) -> dict:
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
            >>> get_content_data("801513ba-a712-498c-8f57-cae55b38cc92")

        Dictionary content
        ------------------
        data = {
            "title": "Kumo desu ga, nani ka?",
            "author": "Miura Kentaro",
            "description": "Some description",
            "cover": "https://uploads.mangadex.org/covers/UID/UID.jpg.512.jpg",
            "genres: ["Ecchi", "BL", "Zombies", "Yuri"],
            "status": "completed" | "ongoing" | "hiatus" | "cancelled",
            "web_link": "https://mangadex.org/title/a96676e58ae2425eb5497f15dd"
            "chapters_data": {
                "total": 100,
                "chapters": [
                    {
                        "title": "Ch.1 - Chapter 1",
                        "date": "2020-01-01",
                        "link": "6310f6a1-17ee-4890-b837-2ec1b372905b",
                        "web_link": "https://mangadex.org/chapter/6310f6a1/"
                        "scanlation": "Band of the Hawks"
                    }
                ]
            }
        }
        """
        # TODO: Status code handler
        payload = {"includes[]": ["cover_art", "author"]}
        api_manga = f"{self.BASE_URL}/manga/{uuid}"

        # Prepare requests
        logger.debug("Requesting manga data...")
        async with self.session.get(api_manga, params=payload) as response:
            logger.debug(f"Requested manga data at {response.url}")
            attrs = (await response.json())["data"]["attributes"]
            relationships = (await response.json())["data"]["relationships"]

        # Collects all manga attributes.
        logger.debug("Getting manga title...")
        title = attrs["title"][list(attrs["title"].keys())[0]]  # First title

        logger.debug("Getting manga description...")
        # If the language is available
        if self.LANG in attrs["description"]:
            description = attrs["description"][self.LANG]
        # If the language is not available, use the first available
        elif isinstance(attrs["description"], dict):
            available_langs = list(attrs["description"].keys())
            # If there is no description, set the value to None
            if not available_langs:
                description = None
            else:
                first_lang = available_langs[0]
                description = attrs["description"][first_lang]
        # If there is no description, set the value to None
        else:
            description = None

        logger.debug("Getting manga cover...")
        cover = [i for i in relationships if i["type"] == "cover_art"][0]
        cover = cover["attributes"]["fileName"]
        cover = f"{self.COVERS_URL}/{uuid}/{cover}.512.jpg"

        logger.debug("Getting manga genres...")
        genres = [genre["attributes"]["name"][list(genre["attributes"]
                  ["name"].keys())[0]] for genre in attrs["tags"]]  # First tag

        logger.debug("Getting manga status...")
        status = attrs["status"]

        logger.debug("Getting manga author...")
        author = [i for i in relationships if i["type"] == "author"][0]
        author = author["attributes"]["name"]

        logger.debug("Getting manga chapters...")
        chapters_data = await self.get_chapters_data(uuid)

        data = {
            "title": title,
            "author": author,
            "description": description,
            "cover": cover,
            "genres": genres,
            "status": status,
            "web_link": f"https://mangadex.org/title/{uuid}",
            "chapters_data": chapters_data
        }

        logger.debug("Done. Returning data...\n")
        return data

    async def get_chapters_data(self, uuid: str,
                                offset: int = 0) -> dict:
        """ Get chapters data. This function is used by get_content_data.

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
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")
        api_chapters = f"{self.BASE_URL}/manga/{uuid}/feed"
        payload = {
            "limit": 500,
            "offset": offset,
            "order[chapter]": "asc",
            "translatedLanguage[]": self.LANG,
            "includes[]": ["scanlation_group", "user"],
            "contentRating[]": ["safe", "suggestive", "erotica",
                                "pornographic"]
        }

        chapters = []

        # Prepare requests
        logger.debug("Requesting chapters data...")
        async with self.session.get(api_chapters, params=payload) as response:
            logger.debug(f"Requested chapters data at {response.url}")
            total = (await response.json())["total"]
            results = (await response.json())["data"]

        logger.debug("Collecting chapters data...\n")

        # Here, we get all the attributes
        for result in results:
            attrs = result["attributes"]
            relation = result["relationships"]

            title = ""
            if attrs["volume"]:
                title += f"Vol.{attrs['volume']}"
            if attrs["chapter"]:
                title += f" Ch.{attrs['chapter']}"
                title = title.strip()
            if attrs["title"]:
                title += f" - {attrs['title']}"

            date = re.match(date_pattern, attrs["publishAt"]).group()
            date = time.strptime(date, "%Y-%m-%d")

            # Scanlation group
            scanlations = [i for i in relation if
                           i["type"] == "scanlation_group"]
            scanlations_list = []
            for scanlation in scanlations:
                scanlations_list.append(scanlation["attributes"]["name"])
            scanlation = " | ".join(scanlations_list)

            # If not scanlation group, we get the user
            if not any(scanlations_list):
                users = [i for i in relation if i["type"] == "user"]
                users_list = []
                for user in users:
                    users_list.append(user["attributes"]["username"])
                scanlation = " | ".join(users_list)

            chapter_id = result["id"]

            if attrs["pages"] > 0:
                chapters.append({
                    "title": title,
                    "date": date,
                    "link": chapter_id,
                    "web_link": f"https://mangadex.org/chapter/{chapter_id}",
                    "scanlation": scanlation
                })

                logger.debug(f"Title: {title} | " +
                             f"Date: {time.strftime('%d/%m/%Y', date)} | " +
                             f"Scanlation: {scanlation}")

        data = {"total": total, "chapters": chapters}

        # If there are more chapters, we get them too
        if total > 500 and offset + 500 < total:
            data["chapters"].extend((await self.get_chapters_data(uuid,
                                     offset + 500))["chapters"])

        logger.debug(f"Done. Returning data... (offset: {offset})")
        return data

    async def get_chapter_images(self, uuid: str) -> list:
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

        api_at_home = f"{self.BASE_URL}/at-home/server/{uuid}"
        images = []

        # Prepare requests
        logger.debug("Requesting chapters data...")
        async with self.session.get(api_at_home) as response:
            logger.debug(f"Requested chapters data at {response.url}")
            base_url = (await response.json())["baseUrl"]
            attributes = (await response.json())["chapter"]

        # Necessary data to make URLs
        logger.debug("Getting chapter hash...")
        hash = attributes["hash"]
        logger.debug("Getting chapter images name...")
        logger.debug(f"Quality mode is \"{self.QUALITY_MODE}\"")
        names = attributes["data" if self.QUALITY_MODE == "data"
                           else "dataSaver"]

        # Making images URLs
        logger.debug("Making images URLs...\n")
        for i, name in enumerate(names):
            image_url = f"{base_url}/{self.QUALITY_MODE}/{hash}/{name}"
            images.append(image_url)
            logger.debug(f"IMAGE {i}: {image_url}\n")

        logger.debug("Done. Returning data...")

        return images

    @searcher_exception_handler
    async def search(
        self,
        limit: int = 25,
        offset: int = None,
        title: str = None,
        authors: list[str] = None,
        artists: list[str] = None,
        year: int = None,
        included_tags: list[str] = [],
        included_tags_mode: str = None,
        excluded_tags: list[str] = [],
        excluded_tags_mode: str = None,
        status: list[str] = None,
        original_language: list[str] = None,
        excluded_original_language: list[str] = None,
        available_translated_language: list[str] = None,
        publication_demographic: list[str] = None,
        ids: list[str] = None,
        content_rating: list[str] = None,
        created_at_since: str = None,
        updated_at_since: str = None,
        order: dict[str, str] = None,
        has_available_chapters: bool = True,
        group: str = None,
        page: int = 1
    ) -> dict:
        """ Search manga, with advanced parameters.
        See: https://api.mangadex.org/swagger.html#/Manga/get-search-manga

        Parameters
        ----------
        limit : int, optional
            Number of results

        offset : int, optional
            Offset between mangas, this will be used to "jump" to the next page

        title : str, optional
            Manga title.

        authors : list[str], optional
            Manga authors (UUID).

        artists : list[str], optional
            Manga artist (UUID).

        year : int, optional
            Manga year.

        included_tags : list[int], optional
            Manga genres.

        included_tags_mode : str, optional
            Genres inclusion mode ("AND" or "OR").

        excluded_tags : list[int], optional
            Manga excluded genres.

        excluded_tags_mode : str, optional
            Excluded genres inclusion mode ("AND" or "OR")

        status : list[str], optional
            Manga status ("ongoing", "completed", "hiatus", "cancelled").

        original_language : list[str], optional
            Manga original language, in ISO 639-1 standard.

        excluded_original_language : list[str], optional
            Manga excluded original language, in ISO 639-1 standard.

        available_translated_language : list[str], optional
            Manga available translated language, in ISO 639-1 standard.

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
            Manga order (
                title: "asc", "desc"
                latestUploadedChapter: "asc", "desc"
                followedCount: "asc", "desc"
                createdAt: "asc", "desc"
                updatedAt: "asc", "desc"
                relevance: "asc", "desc"
                year: "asc", "desc")

        has_available_chapters : bool, optional
            Manga has available chapters.

        group : str, optional
            Manga scanlation group (UUID).

        Returns
        -------
        dict
            Dictionary with all manga results.

        Example
        -------
            >>> search(title="Kumo", order={"updatedAt": "asc"})

        Tags list
        ---------
        0 = Action,
        1 = Adaptation,
        2 = Adventure,
        3 = Aliens,
        4 = Animals,
        5 = Anthology,
        6 = Award Winning,
        7 = Boy's Love,
        8 = Comedy,
        9 = Cooking,
        10 = Crime,
        11 = Crossdressing,
        12 = Delinquents,
        13 = Demons,
        14 = Doujinshi,
        15 = Drama,
        16 = Fan Colored,
        17 = Fantasy,
        18 = 4-Koma,
        19 = Full Color,
        20 = Genderswap,
        21 = Ghosts,
        22 = Girl's Love,
        23 = Gore,
        24 = Gyaru,
        25 = Harem,
        26 = Historical,
        27 = Horror,
        28 = Incest,
        29 = Isekai,
        30 = Loli,
        31 = Long Strip,
        32 = Mafia,
        33 = Magic,
        34 = Magical Girls,
        35 = Martial Arts,
        36 = Mecha,
        37 = Medical,
        38 = Military,
        39 = Monster Girls,
        40 = Monsters,
        41 = Music,
        42 = Mystery,
        43 = Ninja,
        44 = Office Workers,
        45 = Official Colored,
        46 = Oneshot,
        47 = Philosophical,
        48 = Police,
        49 = Post-Apocalyptic,
        50 = Psychological,
        51 = Reincarnation,
        52 = Reverse Harem,
        53 = Romance,
        54 = Samurai,
        55 = School Life,
        56 = Sci-Fi,
        57 = Sexual Violence,
        58 = Shota,
        59 = Slice of Life,
        60 = Sports,
        61 = Superhero,
        62 = Supernatural,
        63 = Survival,
        64 = Thriller,
        65 = Time Travel,
        66 = Tragedy,
        67 = Traditional Games,
        68 = User Created,
        69 = Vampires,
        70 = Video Games,
        71 = Villainess,
        72 = Virtual Reality,
        73 = Web Comic,
        74 = Wuxia,
        75 = Zombies,
        """
        # TODO: Status code handler
        # Included and excluded tags "translator"
        for i, included_tag in enumerate(included_tags):
            included_tags[i] = self.TAGS[included_tag]
        for i, excluded_tag in enumerate(excluded_tags):
            excluded_tags[i] = self.TAGS[excluded_tag]

        available_translated_language = self.LANG  # Set to LANG

        # Query strings
        payload = {
            "limit": limit,
            "offset": limit * (page - 1),
            "title": title,
            "authors[]": authors,
            "artists[]": artists,
            "year": year,
            "includedTags[]": included_tags,
            "includedTagsMode": included_tags_mode,
            "excludedTags[]": excluded_tags,
            "excludedTagsMode": excluded_tags_mode,
            "status[]": status,
            "originalLanguage[]": original_language,
            "excludedOriginalLanguage[]": excluded_original_language,
            "availableTranslatedLanguage[]": available_translated_language,
            "publicationDemographic[]": publication_demographic,
            "ids[]": ids,
            "contentRating[]": content_rating,
            "createdAtSince": created_at_since,
            "updatedAtSince": updated_at_since,
            ("order" if order is None else f"order[{list(order.keys())[0]}]"):
            (order if order is None else order[list(order.keys())[0]]),
            "hasAvailableChapters": "true" if has_available_chapters else
                                    "false",
            "group": group,
            "includes[]": ["cover_art"]
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        data = []  # To store searches

        # Prepare requests
        logger.debug("Requesting search...")
        async with self.session.get(self.BASE_URL + "/manga",
                                    params=payload) as response:
            logger.debug(f"Requested search at {response.url}")
            results = (await response.json())["data"]
            logger.debug(f"Total result: {(await response.json())['total']}\n")

        for result in results:
            attributes = result["attributes"]
            relationships = result["relationships"]

            title = attributes["title"][list(attributes["title"].keys())[0]]
            link = result["id"]

            # Get manga cover
            cover = [i for i in relationships if i["type"] == "cover_art"][0]
            cover = cover["attributes"]["fileName"]
            cover = f"{self.COVERS_URL}/{link}/{cover}.256.jpg"

            logger.debug(f"Title {title}")
            logger.debug(f"Link {link}")
            logger.debug(f"Cover {cover}\n")

            data.append({
                "title": title,
                "link": link,
                "web_link": f"https://mangadex.org/title/{link}",
                "cover": cover
            })

        logger.debug("Done. Returning data...")
        return data

    def get_advanced_search_controls(self) -> dict | None:
        title = {
            "name": "Title",
            "type": "textfield",
            "parameter": "title",
        }
        year = {
            "name": "Year",
            "type": "textfield",
            "parameter": "year",
            "validator": {
                "type": "int",
                "min": 1814,
                "max": time.localtime().tm_year
            }
        }
        included_tags_mode = {
            "name": "Included tags mode",
            "type": "combobox",
            "parameter": "included_tags_mode",
            "content": [
                {"name": "AND", "parameter": "AND"},
                {"name": "OR", "parameter": "OR"}
            ]
        }
        excluded_tags_mode = {
            "name": "Excluded tags mode",
            "type": "combobox",
            "parameter": "excluded_tags_mode",
            "content": [
                {"name": "AND", "parameter": "AND"},
                {"name": "OR", "parameter": "OR"}
            ]
        }
        original_language = {
            "name": "Original language",
            "type": "checkbox",
            "parameter": "original_language",
            "content": [
                {"name": "Japanese", "parameter": "ja"},
                {"name": "Chinese", "parameter": ["zh", "zh-hk"]},
                {"name": "Korean", "parameter": "ko"}
            ]
        }
        status = {
            "name": "Status",
            "type": "checkbox",
            "parameter": "status",
            "content": [
                {"name": "Ongoing", "parameter": "ongoing"},
                {"name": "Completed", "parameter": "completed"},
                {"name": "Hiatus", "parameter": "hiatus"},
                {"name": "Cancelled", "parameter": "cancelled"}
            ]
        }
        publication_demographic = {
            "name": "Publication demographic",
            "type": "checkbox",
            "parameter": "publication_demographic",
            "content": [
                {"name": "Shounen", "parameter": "shounen"},
                {"name": "Shoujo", "parameter": "shoujo"},
                {"name": "Seinen", "parameter": "seinen"},
                {"name": "Josei", "parameter": "josei"},
                {"name": "None", "parameter": "none"}
            ]
        }
        content_rating = {
            "name": "Content rating",
            "type": "checkbox",
            "parameter": "content_rating",
            "content": [
                {"name": "Safe", "parameter": "safe"},
                {"name": "Suggestive", "parameter": "suggestive"},
                {"name": "Erotica", "parameter": "erotica"},
                {"name": "Pornographic", "parameter": "pornographic"},
            ]
        }
        genres = {
            "name": "Genres",
            "type": "tristate-checkbox",
            "checked_parameter": "included_tags",
            "unchecked_parameter": "excluded_tags",
            "content": [
                {"name": "Action", "parameter": 0},
                {"name": "Adaptation", "parameter": 1},
                {"name": "Adventure", "parameter": 2},
                {"name": "Aliens", "parameter": 3},
                {"name": "Animals", "parameter": 4},
                {"name": "Anthology", "parameter": 5},
                {"name": "Award Winning", "parameter": 6},
                {"name": "Boy's Love", "parameter": 7},
                {"name": "Comedy", "parameter": 8},
                {"name": "Cooking", "parameter": 9},
                {"name": "Crime", "parameter": 10},
                {"name": "Crossdressing", "parameter": 11},
                {"name": "Delinquents", "parameter": 12},
                {"name": "Demons", "parameter": 13},
                {"name": "Doujinshi", "parameter": 14},
                {"name": "Drama", "parameter": 15},
                {"name": "Fan Colored", "parameter": 16},
                {"name": "Fantasy", "parameter": 17},
                {"name": "4-Koma", "parameter": 18},
                {"name": "Full Color", "parameter": 19},
                {"name": "Genderswap", "parameter": 20},
                {"name": "Ghosts", "parameter": 21},
                {"name": "Girl's Love", "parameter": 22},
                {"name": "Gore", "parameter": 23},
                {"name": "Gyaru", "parameter": 24},
                {"name": "Harem", "parameter": 25},
                {"name": "Historical", "parameter": 26},
                {"name": "Horror", "parameter": 27},
                {"name": "Incest", "parameter": 28},
                {"name": "Isekai", "parameter": 29},
                {"name": "Loli", "parameter": 30},
                {"name": "Long Strip", "parameter": 31},
                {"name": "Mafia", "parameter": 32},
                {"name": "Magic", "parameter": 33},
                {"name": "Magical Girls", "parameter": 34},
                {"name": "Martial Arts", "parameter": 35},
                {"name": "Mecha", "parameter": 36},
                {"name": "Medical", "parameter": 37},
                {"name": "Military", "parameter": 38},
                {"name": "Monster Girls", "parameter": 39},
                {"name": "Monsters", "parameter": 40},
                {"name": "Music", "parameter": 41},
                {"name": "Mystery", "parameter": 42},
                {"name": "Ninja", "parameter": 43},
                {"name": "Office Workers", "parameter": 44},
                {"name": "Official Colored", "parameter": 45},
                {"name": "Oneshot", "parameter": 46},
                {"name": "Philosophical", "parameter": 47},
                {"name": "Police", "parameter": 48},
                {"name": "Post-Apocalyptic", "parameter": 49},
                {"name": "Psychological", "parameter": 50},
                {"name": "Reincarnation", "parameter": 51},
                {"name": "Reverse Harem", "parameter": 52},
                {"name": "Romance", "parameter": 53},
                {"name": "Samurai", "parameter": 54},
                {"name": "School Life", "parameter": 55},
                {"name": "Sci-Fi", "parameter": 56},
                {"name": "Sexual Violence", "parameter": 57},
                {"name": "Shota", "parameter": 58},
                {"name": "Slice of Life", "parameter": 59},
                {"name": "Sports", "parameter": 60},
                {"name": "Superhero", "parameter": 61},
                {"name": "Supernatural", "parameter": 62},
                {"name": "Survival", "parameter": 63},
                {"name": "Thriller", "parameter": 64},
                {"name": "Time Travel", "parameter": 65},
                {"name": "Tragedy", "parameter": 66},
                {"name": "Traditional Games", "parameter": 67},
                {"name": "User Created", "parameter": 68},
                {"name": "Vampires", "parameter": 69},
                {"name": "Video Games", "parameter": 70},
                {"name": "Villainess", "parameter": 71},
                {"name": "Virtual Reality", "parameter": 72},
                {"name": "Web Comic", "parameter": 73},
                {"name": "Wuxia", "parameter": 74},
                {"name": "Zombies", "parameter": 75}
            ]
        }
        order = {
            "name": "Order",
            "type": "ascDescMap",
            "parameter": "order",
            "asc_parameter": "asc",
            "desc_parameter": "desc",
            "default_param": {
                "name": "latestUploadedChapter",
                "parameter": "desc"
            },
            "content": [
                {"name": "Alphabetic", "parameter": "title"},
                {"name": "Chapter uploaded date",
                 "parameter": "latestUploadedChapter"},
                {"name": "Number of follows", "parameter": "followedCount"},
                {"name": "Created date", "parameter": "createdAt"},
                {"name": "Updated date", "parameter": "updatedAt"},
                {"name": "Popularity", "parameter": "relevance"},
                {"name": "Year", "parameter": "year"},
            ]
        }

        return [title, year, included_tags_mode, excluded_tags_mode, status,
                publication_demographic, content_rating, original_language,
                genres, order]

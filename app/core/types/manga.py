class Chapter:
    """ Chapter type to be used in Manga class """
    def __init__(self, scraper, name: str, date: list[str, str, str],
                 link: str, scanlation: str) -> None:
        self.scraper = scraper
        self.name = name
        self.date = date
        self.link = link
        self.scanlation = scanlation

    def get_images(self) -> list[str]:
        """ Get images from chapter """
        return self.scraper.get_chapter_images(self.link)


class ChaptersData:
    """ Chapters data type to be used in Manga class """
    def __init__(self, total: int, chapters: list[Chapter]) -> None:
        self.total = total
        self.chapters = chapters


class Manga:
    """ Manga type to get all manga data """
    def __init__(self, scraper, title: str, author: str, description: str,
                 cover: str, genres: list[str], status: str, link: str,
                 chapters_data: ChaptersData) -> None:
        self.scraper = scraper
        self.title = title
        self.author = author
        self.description = description
        self.cover = cover
        self.genres = genres
        self.status = status
        self.link = link
        self.chapters_data = chapters_data


class MangaSearch:
    """ Manga search type """
    def __init__(self, scraper, title: str, link: str, cover: str) -> None:
        self.scraper = scraper
        self.title = title
        self.link = link
        self.cover = cover

    def get_data(self) -> Manga:
        """ Get manga data """
        data = self.scraper.get_manga_data(self.link)

        title = data["title"]
        author = data["author"]
        description = data["description"]
        cover = data["cover"]
        genres = data["genres"]
        status = data["status"]
        chapters = []
        for chapter in data["chapters_data"]["chapters"]:
            chapters.append(
                Chapter(
                    self.scraper,
                    chapter["name"],
                    chapter["date"],
                    chapter["link"],
                    chapter["scanlation"],
                )
            )
        chapters_data = ChaptersData(data["chapters_data"]["total"], chapters)

        manga = Manga(
            self.scraper,
            title, author, description, cover, genres, status, self.link,
            chapters_data
        )

        return manga

from PyQt5.QtCore import QObject, QVariant, pyqtSlot, pyqtProperty


class Chapter(QObject):
    """ Chapter type to be used in Manga class """
    def __init__(self, scraper, name: str, date: list[str, str, str],
                 link: str, scanlation: str, parent) -> None:
        super(Chapter, self).__init__(parent)

        self._scraper = scraper
        self._name = name
        self._date = date
        self._link = link
        self._scanlation = scanlation

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str)
    def name(self) -> str:
        return self._name

    @pyqtProperty(list)
    def date(self) -> list:
        return self._date

    @pyqtProperty(str)
    def link(self) -> str:
        return self._link

    @pyqtProperty(str)
    def scanlation(self) -> str:
        return self._scanlation

    @pyqtSlot(result=list)
    def get_images(self) -> list[str]:
        """ Get images from chapter """
        return self._scraper.get_chapter_images(self._link)


class ChaptersData(QObject):
    """ Chapters data type to be used in Manga class """
    def __init__(self, total: int, chapters: list[Chapter], parent) -> None:
        super(ChaptersData, self).__init__(parent)

        self._total = total
        self._chapters = chapters

    @pyqtProperty(int)
    def total(self) -> int:
        return self._total

    @pyqtProperty(QVariant)
    def chapters(self) -> list[Chapter]:
        return self._chapters


class Manga(QObject):
    """ Manga type to get all manga data """
    def __init__(self, scraper, title: str, author: str, description: str,
                 cover: str, genres: list[str], status: str, link: str,
                 chapters_data: ChaptersData, parent) -> None:
        super(Manga, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._author = author
        self._description = description
        self._cover = cover
        self._genres = genres
        self._status = status
        self._link = link
        self._chapters_data = chapters_data

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str)
    def title(self) -> str:
        return self._title

    @pyqtProperty(str)
    def author(self) -> str:
        return self._author

    @pyqtProperty(str)
    def description(self) -> str:
        return self._description

    @pyqtProperty(str)
    def cover(self) -> str:
        return self._cover

    @pyqtProperty(list)
    def genres(self) -> list[str]:
        return self._genres

    @pyqtProperty(str)
    def status(self) -> str:
        return self._status

    @pyqtProperty(str)
    def link(self) -> str:
        return self._link

    @pyqtProperty(QVariant)
    def chapters_data(self) -> ChaptersData:
        return self._chapters_data


class MangaSearch(QObject):
    """ Manga search type """
    def __init__(self, scraper, title: str, link: str, cover: str, parent):
        super(MangaSearch, self).__init__(parent)

        self._scraper = scraper
        self._title = title
        self._link = link
        self._cover = cover

    @pyqtProperty(str)
    def scraper(self) -> str:
        return self._scraper.NAME

    @pyqtProperty(str)
    def title(self) -> str:
        return self._title

    @pyqtProperty(str)
    def link(self) -> str:
        return self._link

    @pyqtProperty(str)
    def cover(self) -> str:
        return self._cover

    @pyqtSlot(result=QVariant)
    def get_data(self) -> Manga:
        """ Get manga data """
        data = self._scraper.get_manga_data(self._link)

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
                    self._scraper,
                    chapter["name"],
                    chapter["date"],
                    chapter["link"],
                    chapter["scanlation"],
                    self
                )
            )
        chapters_data = ChaptersData(data["chapters_data"]["total"], chapters,
                                     self)

        manga = Manga(
            self._scraper,
            title, author, description, cover, genres, status, self._link,
            chapters_data, self
        )

        return QVariant(manga)

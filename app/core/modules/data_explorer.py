from ..types import Manga


class DataExplorer(Manga):
    def __init__(self, data: Manga):
        keys = locals()["data"].__dict__
        data_dict = {
            "scraper": keys["_scraper"],
            "title": keys["_title"],
            "author": keys["_author"],
            "description": keys["_description"],
            "cover": keys["_cover"],
            "genres": keys["_genres"],
            "link": keys["_link"],
            "parent": keys["_parent"],
            "status": keys["_status"],
            "chapters_data": keys["_chapters_data"],
        }

        super().__init__(**data_dict)

from ..types import Manga


class DataExplorer(Manga):
    def __init__(self, data: Manga):
        data_values = locals()["data"].__dict__.values()
        super(DataExplorer, self).__init__(*data_values)

import os

from importlib import import_module, reload
from functools import wraps
from pathlib import Path

from PyQt5.QtCore import QObject, QVariant, pyqtProperty
from PyQt5 import QtQuick, QtQml
from aiohttp import ClientSession
from qasync import asyncSlot

from core.types import MangaSearch, SignalHandler
from core import scrapers
QtQuick


def set_searching(qasync_func):
    @wraps(qasync_func)
    def wrapper(func):
        @wraps(func)
        async def wrapped(self, *args, **kwargs):
            # If the search is already running, don't run it again
            if self._searching:
                return
            # Set the search to running
            try:
                self._searching = True
                await func(self, *args, **kwargs)  # Run the function
            # Finally, set the search to not running
            finally:
                self._searching = False
        return qasync_func(wrapped)
    return wrapper


class Explorer(SignalHandler, QObject):
    def __init__(self, session: ClientSession, signals_handler: SignalHandler,
                 parent=None) -> None:
        super(Explorer, self).__init__(parent)

        self._session = session
        self._scraper = self.get_scrapers()[0]
        self._signals_handler = signals_handler
        self._searching = False

    # Get as input the search type, search root and page index
    @set_searching(asyncSlot(str, QObject, int))  # Decorator to set searching
    async def search_manga(self, search_type: str, search_root: QObject,
                           page: int):
        """
        Search for manga using the given search type and search root.

        Posibles search types are: empty, to search for all manga; title, to
        search for a manga by title; advanced, to search for a manga by
        advanced search.
        """

        # If the search type is empty, do a search empty search
        if search_type == "empty":
            data = await self._scraper.search_manga(page=page)
        # If the search type is title, do a search by title
        elif search_type == "title":
            title = search_root.property("searchText")
            data = await self._scraper.search_manga(title=title, page=page)
        # If the search type is advanced, do a search by advanced search
        elif search_type == "advanced":
            parameters = {}
            components = search_root.property("contentItem").childItems()
            one_iter = ["textField", "comboBox", "slider"]

            # Loop through the search controls (textfield, combobox, slider...)
            for component in components:
                if component.objectName() in one_iter:
                    param = component.property("parameter")
                    value = component.property("value")
                    parameters[param] = value  # Add the parameter to the dict

                elif component.objectName() == "tristate-checkBox":
                    checked_param = component.property("checkedParameter")
                    unchecked_param = component.property("uncheckedParameter")
                    parameters[checked_param] = []
                    parameters[unchecked_param] = []

                    list_view = component.childItems()[1]
                    delegates = list_view.property("contentItem").childItems()

                    # Loop through the list view check delegates
                    for delegate in delegates:
                        # If the delegate is checked, add the parameter to the
                        # checked parameters list
                        if delegate.property("parameter") == checked_param:
                            value = delegate.property("value")
                            # If value is a list, append all values to params
                            if type(value) == QtQml.QJSValue:
                                values = value.toVariant()
                                for value in values:
                                    parameters[checked_param].append(value)
                            else:
                                parameters[checked_param].append(value)
                        # If the delegate is unchecked, add the parameter to
                        # the unchecked parameters list
                        elif delegate.property("parameter") == unchecked_param:
                            value = delegate.property("value")
                            # If value is a list, append all values to params
                            if type(value) == QtQml.QJSValue:
                                values = value.toVariant()
                                for value in values:
                                    parameters[unchecked_param].append(value)
                            else:
                                parameters[unchecked_param].append(value)

                elif component.objectName() == "checkBox":
                    param = component.property("parameter")
                    parameters[param] = []

                    list_view = component.childItems()[1]
                    delegates = list_view.property("contentItem").childItems()

                    for delegate in delegates:
                        # If the delegate is checked, add the parameter to the
                        # checked parameters list
                        if delegate.property("parameter") == param:
                            value = delegate.property("value")
                            # If value is a list, append all values to params
                            if type(value) == QtQml.QJSValue:
                                values = value.toVariant()
                                for value in values:
                                    parameters[param].append(value)
                            else:
                                parameters[param].append(value)

            parameters["page"] = page  # Add the page to the parameters dict
            data = await self._scraper.search_manga(**parameters)

        results = []
        for result in data:
            title = result["title"]
            link = result["link"]
            cover = result["cover"]

            results.append(MangaSearch(self._scraper, title, link, cover,
                                       self))

        self._signals_handler.mangaSearch.emit(results)

    @pyqtProperty(str)
    def scraper(self) -> object:
        return self._scraper.NAME

    @scraper.setter
    def scraper(self, scraper: str) -> None:
        for class_obj in self.get_scrapers():
            if class_obj.NAME == scraper:
                self._scraper = class_obj
                break

    @pyqtProperty(list, constant=True)
    def scrapers_list(self) -> list:
        scrapers_list = []
        for scraper in self.get_scrapers():
            scrapers_list.append(scraper.NAME)

        return scrapers_list

    def get_scrapers(self) -> list:
        classes = []
        for file in Path(scrapers.__path__[0]).glob("*.py"):
            name = os.path.splitext(os.path.basename(file))[0]
            module = reload(import_module(f"{scrapers.__name__}.{name}"))

            for attr in dir(module):
                class_obj = getattr(module, attr)
                if hasattr(class_obj, "get_manga_data"):
                    classes.append(class_obj(self._session))

        return classes

    @pyqtProperty(QVariant, constant=True)
    def advanced_search(self) -> list:
        return self._scraper.advanced_search_controls()

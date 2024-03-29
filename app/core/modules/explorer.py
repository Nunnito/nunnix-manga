import asyncio
import os


from importlib import import_module, reload
from functools import wraps
from pathlib import Path

from PyQt5.QtCore import QObject, QVariant, pyqtProperty
from PyQt5 import QtQuick, QtQml  # noqa: F401
from qasync import asyncSlot

from aiohttp.client_exceptions import ClientConnectorError
from aiohttp import ClientSession

from ..types import MangaSearch
from ..utils import SignalHandler, logger
from .. import utils
from .. import scrapers


def search_deco(qasync_func):
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

            # If an exception is raised, do the following
            except Exception as e:
                exception_info = {"is_exception": True, "exception": {}}
                exception_info["exception"]["message"] = str(e)

                # Connection error
                if isinstance(e, ClientConnectorError):
                    logger.error("Connection error")
                    logger.error(e)
                    exception_info["exception"]["type"] = "connection_error"
                # Timeout error
                elif isinstance(e, asyncio.TimeoutError):
                    logger.error("Timeout error")
                    exception_info["exception"]["type"] = "timeout_error"
                # Other errors
                else:
                    logger.error(e)
                    exception_info["exception"]["type"] = "unknown_error"

                # Emit the signal with the exception info
                self._signals_handler.searchResult.emit(exception_info)

            # Finally, set the search to not running
            finally:
                self._searching = False
        return qasync_func(wrapped)
    return wrapper


def advanced_search_deco(pyqt_property):
    @wraps(pyqt_property)
    def wrapper(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            # Try to return advanced search controls
            try:
                return func(self, *args, **kwargs)
            # If a exception is raised, show in the advanced search controls UI
            except Exception as e:
                exception_label = {
                    "type": "label",
                    "bold": True,
                    "content": str(e)
                }
                return [exception_label]
        return pyqt_property(wrapped)
    return wrapper


class Explorer(SignalHandler, QObject):
    def __init__(self, session: ClientSession, signals_handler: SignalHandler,
                 parent=None) -> None:
        super(Explorer, self).__init__(parent)

        self._session = session
        self._scraper = self.get_scrapers()[0]
        self._signals_handler = signals_handler
        self._searching = False

    # Get as input the search type, roo explorer QML object and page index
    @search_deco(asyncSlot(str, QObject, int))
    async def search(self, search_type: str, explorer: QObject,
                     page: int):
        """
        Search using the given search type and explorer QML Object.

        Posibles search types are: empty, to search all; title, to
        search by title; advanced, to search by advanced search.
        """
        # Set exceptions variables to false
        explorer.setProperty("noResults", False)
        explorer.setProperty("endOfResults", False)
        explorer.setProperty("connectionError", False)
        explorer.setProperty("timeOutError", False)
        explorer.setProperty("unknownError", False)

        search_root = explorer.property("searchRoot")  # Get the search root

        parameters = {}  # Create a dict to store the parameters

        # If the search type is empty, do a empty search
        if search_type == "empty":
            pass
        # If the search type is title, do a search by title
        elif search_type == "title":
            title = search_root.property("searchText")
            parameters["title"] = title
        # If the search type is advanced, do a search by advanced search
        elif search_type == "advanced":
            advanced_params = self.get_advanced_search_parameters(search_root)
            parameters.update(advanced_params)

        parameters["page"] = page  # Add the page to the parameters dict
        data = await self._scraper.search(**parameters)

        # If the data contains a dict with exceptions, emit it
        if type(data) == dict:
            self._signals_handler.searchResult.emit(data)
        else:
            results = []
            for result in data:
                title = result["title"]
                link = result["link"]
                web_link = result["web_link"]
                cover = await utils.Thumbnails.get_thumbnail(result["cover"],
                                                             self.scraper,
                                                             self._session)

                if self._scraper.TYPE == "manga":
                    results.append(MangaSearch(self._scraper, title, link,
                                               web_link, cover, self))

            self._signals_handler.searchResult.emit(results)

    def get_advanced_search_parameters(self, search_root: QObject) -> dict:
        """
        Get the advanced search parameters from the given explorer QML object.
        """
        parameters = {}  # Create a dict to store the parameters

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

            elif component.objectName() == "ascDescMap":
                param = component.property("parameter")  # URL parameter
                # Values parameter of the dictionary
                asc_param = component.property("ascParameter")
                desc_param = component.property("descParameter")
                parameters[param] = {}  # Create the dictionary

                list_view = component.childItems()[1]
                delegates = list_view.property("contentItem").childItems()

                for delegate in delegates:
                    # If the delegate is checked, add the parameter to the
                    # checked parameters list
                    if delegate.property("parameter") == param:
                        # Key parameter of the dictionary
                        value = delegate.property("value")
                        # If the checkbox is ascendent
                        if delegate.property("subParameter") == asc_param:
                            parameters[param][value] = asc_param
                        # If the checkbox is descendent
                        else:
                            parameters[param][value] = desc_param

        return parameters

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
        for file in Path(scrapers.__path__[0]).glob("*/*.py"):
            dir_name = os.path.basename(file.parent)
            name = os.path.splitext(os.path.basename(file))[0]
            module = import_module(f"{scrapers.__name__}.{dir_name}.{name}")
            module = reload(module)

            for attr in dir(module):
                class_obj = getattr(module, attr)
                if hasattr(class_obj, "TYPE"):
                    classes.append(class_obj(self._session))

        return classes

    @advanced_search_deco(pyqtProperty(QVariant, constant=True))
    def advanced_search(self) -> list:
        return self._scraper.get_advanced_search_controls()

import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../components" as C
import "components"

SplitView {
    property string name: "explore"
    property alias searchColumn: searchColumn
    property alias grid: grid
    property alias topBar: topBar
    property alias searchModel: searchModel
    property alias advancedSearch: advancedSearch

    property bool noResults: false
    property bool endOfResults: false
    property bool connectionError: false
    property bool timeOutError: false
    property bool unknownError: false
    property string errorMessage

    property int currentPage: 1  // Set to 1 to start with the first page 
    property string searchType
    property var searchRoot: {
        if (searchType == "empty" || searchType == "title") {
            return topBar.searchField
        }
        else if (searchType == "advanced") {
            return advancedSearch.controls
        }
    }

    id: explorer
    clip: true

    // Top bar and container
    Column {
        id: searchColumn

        SplitView.fillWidth: true
        SplitView.minimumWidth: parent.width - advancedSearch._width
        SplitView.preferredWidth: parent.width
        
        TopBar {id: topBar}
        SearchContainer {id: grid}
        ListModel {id: searchModel; property var getData: ({})}
        StatusBar {id: statusBar}
    }

    // Right side container for advanced search
    AdvancedSearch {id: advancedSearch}
    handle: Item {}  // Invisible item to handle the drag

    // Connections
    Connections {
        target: SignalHandler
        function onSearchResult(searchResult) {
            if (searchResult.is_exception) {
                if (searchResult.exception.type == "no_results") {
                    noResults = true
                }
                else if (searchResult.exception.type == "end_of_results") {
                    endOfResults = true
                }
                else if (searchResult.exception.type == "connection_error") {
                    connectionError = true
                }
                else if (searchResult.exception.type == "timeout_error") {
                    timeOutError = true
                }
                else if (searchResult.exception.type == "unknown_error") {
                    unknownError = true
                }
                errorMessage = searchResult.exception.message
            }
            else {
                for (var i = 0; i < searchResult.length; i++) {
                    let search = searchResult[i].jsonObject
                    let getData = searchResult[i].get_data  // get_data function
                    // Add getData function to the getData dictionary
                    searchModel.getData[searchModel.count] = ()=>{getData()}
                    search.index = searchModel.count

                    searchModel.append(search)  // Append the search to the model
                }
            }
        }
    }

    // When the component is created
    Component.onCompleted: {
        searchType = "empty"
        Explorer.search(searchType, explorer, currentPage)
    }

    // Shortcut to reload
    Shortcut {
        autoRepeat: false
        sequence: "F5"
        enabled: visible

        onActivated: {
            explorer.searchModel.clear()  // Clear search results
            explorer.currentPage = 1  // Reset page to 1
            Explorer.search(searchType, explorer, currentPage)  // Do search
        }
    }
}

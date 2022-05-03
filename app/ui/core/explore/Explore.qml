import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../components" as C
import "components"

SplitView {
    property string name: "explore"
    property alias searchColumn: searchColumn
    property alias grid: grid
    property alias topBar: topBar
    property alias searchModel: searchModel
    property alias advancedSearch: advancedSearch

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

    // Top bar and container for mangas
    Column {
        id: searchColumn

        SplitView.fillWidth: true
        SplitView.minimumWidth: parent.width - advancedSearch._width
        SplitView.preferredWidth: parent.width
        
        TopBar {id: topBar}
        SearchContainer {id: grid}
        ListModel {id: searchModel}
        StatusBar {id: statusBar}
    }

    // Right side container for advanced search
    AdvancedSearch {id: advancedSearch}
    handle: Item {}  // Invisible item to handle the drag

    // Connections
    Connections {
        target: SignalHandler
        function onMangaSearch(mangaSearch) {
            for (var i = 0; i < mangaSearch.length; i++) {
                searchModel.append(mangaSearch[i].jsonObject)
            }
        }
    }

    // When the component is created
    Component.onCompleted: {
        searchType = "empty"
        Explorer.search_manga(searchType, searchRoot, currentPage)
    }
}

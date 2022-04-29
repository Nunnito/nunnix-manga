import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../components" as C
import "components"

SplitView {
    property string name: "explore"
    property alias searchColumn: searchColumn
    property alias grid: grid
    property alias searchModel: searchModel
    property alias advancedSearch: advancedSearch
    property var searchParams: ({})  // Search params in JSON format

    id: explorer
    clip: true

    // Top bar and container for mangas
    Column {
        id: searchColumn

        SplitView.fillWidth: true
        SplitView.minimumWidth: parent.width - 300  // 300 is the advanced search width
        SplitView.preferredWidth: parent.width
        
        TopBar {id: topBar}
        SearchContainer {id: grid}
        ListModel {id: searchModel}
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
        searchParams["page"] = 1  // Set the page to 1
        Explorer.search_manga(searchParams)
    }
}

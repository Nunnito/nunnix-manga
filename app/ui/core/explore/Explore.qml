import QtQuick 2.15
import "../../components" as C
import "components"

Column {
    property string name: "explore"
    property var searchParams: ({})  // Search params in JSON format
    property alias grid: grid
    property alias searchModel: searchModel

    id: explorer
    
    TopBar {id: topBar}
    SearchContainer {id: grid}
    ListModel {id: searchModel}

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

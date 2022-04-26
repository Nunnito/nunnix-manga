import QtQuick 2.15
import "../../components" as C
import "components"

Column {
    property string name: "explore"
    property alias grid: grid

    id: explorer
    
    TopBar {id: topBar}
    SearchContainer {id: grid}

    Connections {
        target: SignalHandler
        function onMangaSearch(mangaSearch) {
            grid.model = mangaSearch
        }
    }

    Component.onCompleted: {
        Explorer.search_manga({})
    }
}

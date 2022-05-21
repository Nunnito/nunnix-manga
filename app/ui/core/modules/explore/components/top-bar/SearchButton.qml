import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../../components" as C
import "../../../../../theme"  // Only for testing, will be removed in the future


C.RoundButton {
    // Color properties
    colorBg: theme.topBarButtonBg
    colorFg: theme.topBarButtonFg
    colorBgOver: theme.topBarButtonBgOver
    colorFgOver: theme.topBarButtonFgOver
    colorBgClick: theme.topBarButtonBgClick
    colorFgClick: theme.topBarButtonFgClick

    icon.source: Icon.get_icon("search.svg")

    onClicked: {
        searchField.searchText = searchField.text
        explorer.searchModel.clear()  // Clear search results
        explorer.currentPage = 1  // Reset page to 1
        explorer.searchType = searchField.text ? "title" : "empty"

        // Do search
        Explorer.search_manga(explorer.searchType, explorer,
                              explorer.currentPage)
    }
}

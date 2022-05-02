import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C


C.RoundButton {
    // Color properties
    colorBg: theme.topBarButtonBg
    colorFg: theme.topBarButtonFg
    colorBgOver: theme.topBarButtonBgOver
    colorFgOver: theme.topBarButtonFgOver
    colorBgClick: theme.topBarButtonBgClick
    colorFgClick: theme.topBarButtonFgClick

    icon.source: Icon.get_icon("filter-list.svg")
    visible: Explorer.advanced_search ? true : false

    onClicked: {
        if (!explorer.advancedSearch.open) {
            explorer.advancedSearch.openAnim.start()
            explorer.grid.width = Qt.binding(function() {
                return explorer.searchColumn.SplitView.minimumWidth
                })
        }
        else {
            explorer.advancedSearch.closeAnim.start()
            explorer.grid.width = Qt.binding(function() {return explorer.width})
        }
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C
import "../../../../theme"  // Only for testing, will be removed in the future


C.RoundButton {
    // Color properties
    colorBg: theme.topBarButtonBg
    colorFg: theme.topBarButtonFg
    colorBgOver: theme.topBarButtonBgOver
    colorFgOver: theme.topBarButtonFgOver
    colorBgClick: theme.topBarButtonBgClick
    colorFgClick: theme.topBarButtonFgClick

    icon.source: Icon.get_icon("filter-list.svg")

    onClicked: theme = theme == Dark ? Light : Dark  // Only for testing
}

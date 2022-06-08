import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../components" as C

C.RoundButton {
    flat: true
    icon.source: Icon.get_icon("bookmark_outlined.svg")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    C.ToolTip {label: qsTr("Save to library"); visible: hovered}
}

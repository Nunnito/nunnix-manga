import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

C.RoundButton {
    flat: true
    icon.source: Icon.get_icon("downloads-outlined.svg")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    C.ToolTip {label: qsTr("Download"); visible: hovered}
}

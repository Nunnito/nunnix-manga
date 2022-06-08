import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../components" as C

C.RoundButton {
    flat: true
    icon.source: Icon.get_icon("menu.svg")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
}

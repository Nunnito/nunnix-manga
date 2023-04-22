import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../components" as C

C.Button {
    flat: true
    icon.source: Icon.get_icon("arrow_drop_down.svg")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
}

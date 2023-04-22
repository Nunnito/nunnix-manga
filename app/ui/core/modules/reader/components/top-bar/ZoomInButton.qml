import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../components" as C

C.Button {
    flat: true
    icon.source: Icon.get_icon("zoom_in.svg")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
}

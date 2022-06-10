import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    text: qsTr("Bookmark")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
}

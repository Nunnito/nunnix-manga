import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    flat: true
    text: qsTr("Cancel")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    onClicked: tbStackView.pop()
}

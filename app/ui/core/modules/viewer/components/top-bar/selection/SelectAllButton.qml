import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../../components" as C

BaseButton {
    highlighted: true
    flat: true
    text: qsTr("Select all")

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
    onClicked: _data.chapters_data.select_all()
}

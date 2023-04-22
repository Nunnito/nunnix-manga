import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../components" as C

C.ComboBox {
    property var sizes: [
        qsTr("Fit Width"),
        qsTr("Fit Height"),
        qsTr("10 %"),
        qsTr("25 %"),
        qsTr("50 %"),
        qsTr("75 %"),
        qsTr("100 %"),
        qsTr("125 %"),
        qsTr("150 %"),
        qsTr("200 %"),
        qsTr("400 %"),
        qsTr("800 %"),
        qsTr("1600 %")
    ]
    flat: true
    model: sizes

    C.CursorShape {cursorShape: Qt.PointingHandCursor}
}

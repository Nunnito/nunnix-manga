import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../../components" as C

Row {
    height: parent.height
    spacing: 8

    C.TextField {
        horizontalAlignment: TextInput.AlignHCenter
        anchors.verticalCenter: parent.verticalCenter
        outlined: true
        width: 64
        text: "1"
    }
    C.Label {
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("of")
    }
    C.Label {
        anchors.verticalCenter: parent.verticalCenter
        text: "100"
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C

Row {
    C.Label {
        text: qsTr("Status: ")
        font.bold: true
        font.pixelSize: 14
    }
    C.Label {
        text: _data ? _data.status : ""
        font.pixelSize: 14
    }
}

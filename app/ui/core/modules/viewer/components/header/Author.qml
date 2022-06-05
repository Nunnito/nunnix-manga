import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C

Row {
    C.Label {
        text: qsTr("Author: ")
        font.bold: true
        font.pixelSize: 14
    }
    C.Label {
        text: _data ? _data.author : ""
        font.pixelSize: 14
    }
}

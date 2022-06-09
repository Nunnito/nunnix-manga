import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C

Row {
    C.Label {
        text: qsTr("Author: ")
        font.bold: true
        font.pixelSize: 14
        visible: _data ? true : false
    }
    C.Label {
        id: author
        text: _data ? _data.author : ""
        font.pixelSize: 14
    }

    // Rectangle placeholder when no data is available
    LoaderPlaceHolder {height: author.height; width: 150}
}

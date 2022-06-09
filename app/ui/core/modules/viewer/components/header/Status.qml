import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C

Row {
    C.Label {
        text: qsTr("Status: ")
        font.bold: true
        font.pixelSize: 14
        visible: _data ? true : false
    }
    C.Label {
        id: status
        text: _data ? _data.status : ""
        font.pixelSize: 14
    }

    // Rectangle placeholder when no data is available
    LoaderPlaceHolder {height: status.height; width: 100}
}

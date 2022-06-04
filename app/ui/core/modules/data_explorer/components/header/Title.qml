import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C

C.Label {
    width: _header.width - (image.width + (row.padding * 2) + row.spacing)

    text: _data ? _data.title : ""
    wrapMode: Label.WordWrap

    font.pixelSize: 24
    font.bold: true
}

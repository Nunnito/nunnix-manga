import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


C.Label {
    property string one_chapter: qsTr("chapter")
    property string many_chapters: qsTr("chapters")
    property int total: listView.count

    leftPadding: 40
    text: total + " " + (total == 1 ? one_chapter : many_chapters) 

    font.pixelSize: 20
    font.bold: true
}

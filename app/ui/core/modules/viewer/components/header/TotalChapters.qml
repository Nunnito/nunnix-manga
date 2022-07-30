import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


Column {
    C.Label {
        property string one_chapter: qsTr("chapter")
        property string many_chapters: qsTr("chapters")
        property int total: listView.count

        id: label

        leftPadding: 40
        text: total + " " + (total == 1 ? one_chapter : many_chapters) 

        font.pixelSize: 20
        font.bold: true
        visible: _data ? true : false

    }

    // Rectangle placeholder when no data is available
    LoaderPlaceHolder {height: label.height; width: 125; x: label.leftPadding}
}

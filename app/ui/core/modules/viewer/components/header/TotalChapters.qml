import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


Column {
    RowLayout {
        width: column.width
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
        C.Spacer {orientation: "horizontal"}

        C.RoundButton {
            flat: true
            icon.source: Icon.get_icon("filter-list.svg")

            Layout.rightMargin: 20
            C.CursorShape {cursorShape: Qt.PointingHandCursor}
        }
    }
    // Rectangle placeholder when no data is available
    LoaderPlaceHolder {height: label.height; width: 125; x: label.leftPadding}
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C

Column {
    width: listView.width
    topPadding: modelData.topPadding ? modelData.topPadding : topPadding
    bottomPadding: modelData.bottomPadding ? modelData.bottomPadding : bottomPadding
    C.Label {
        width: modelData.centered ? contentWidth : parent.width
        wrapMode: Text.WordWrap
        text: modelData.content
        font.bold: modelData.bold ? true : false
        anchors.horizontalCenter: parent.horizontalCenter
    }
}

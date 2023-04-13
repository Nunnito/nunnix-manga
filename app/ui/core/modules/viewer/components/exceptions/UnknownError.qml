import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../../components" as C


Item {
    anchors.centerIn: parent
    visible: unknownError

    Column {
        width: rootWindow.width
        C.Label {
            text: qsTr("Unknown error: %1").arg(exceptionMessage) 
            anchors.horizontalCenter: parent.horizontalCenter
            font.bold: true
            font.pixelSize: 18
        }
        ExceptionButton {}
        x: -(width / 2)
    }
}

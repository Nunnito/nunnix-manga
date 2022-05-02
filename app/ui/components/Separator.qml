import QtQuick 2.15
import QtQuick.Controls 2.15

Column {
    property var color: theme.separator
    MenuSeparator {

        width: parent.width
        contentItem: Rectangle {
            implicitWidth: parent.width
            implicitHeight: 1
            color: parent.color
        }
    }
}

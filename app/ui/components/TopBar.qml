import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Item {
    width: parent.width

    Rectangle {
        width: parent.width
        height: 48
        color: theme.topBarBg
        // Pane for elevation shadow
        Pane {
            anchors.fill: parent
            Material.background: parent.color
            Material.elevation: 3
        }
    }
}

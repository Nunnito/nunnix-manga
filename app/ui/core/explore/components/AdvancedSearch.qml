import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Pane {
    property alias openAnim: openAnim
    property alias closeAnim: closeAnim
    property bool open: width > 0

    x: parent.width - width

    Material.background: theme.controlBg
    SplitView.minimumWidth: item.width  // To animate the pane
    SplitView.preferredWidth: 0  // Initially hidden

    ListView {
        anchors.fill: parent
    }

    Item {id: item; width: 0}  // To animate the pane

    // Open and close animations
    PropertyAnimation {
        id: openAnim
        target: item
        properties: "width"
        duration: 500
        to: 300
        easing.type: Easing.OutQuint
    }
    PropertyAnimation {
        id: closeAnim
        target: item
        properties: "width"
        duration: 500
        to: 0
        easing.type: Easing.OutQuint
    }
}

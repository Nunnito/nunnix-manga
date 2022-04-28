import QtQuick 2.15

MouseArea {
    hoverEnabled: true
    onPressed: mouse.accepted = false

    anchors.fill: parent
}

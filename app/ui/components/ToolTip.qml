import QtQuick 2.15
import QtQuick.Controls 2.15 as Controls

Controls.ToolTip {
    property alias label: label.text
    delay: 1000
    timeout: 5000

    Label {
        id: label
        font.pixelSize: 14
    }
    background: Rectangle {
        color: theme.controlBg
        radius: 2
    }
}

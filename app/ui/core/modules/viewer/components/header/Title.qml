import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C

Flickable {
    id: title
    width: _header.width - (image.width + (row.padding * 2) + row.spacing)
    height: label.contentHeight

    contentWidth: label.contentWidth
    clip: true

    C.Label {
        id: label

        width: parent.width
        height: parent.height

        text: _data ? _data.title : ""
        font.pixelSize: 24
        font.bold: true

        C.ToolTip {visible: hovered; label: _data ? _data.title : ""}

        // MouseArea to start the scroll text animation
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true

            onEntered: {
                if (title.contentWidth > title.width) {
                    backAnimation.stop()
                    startAnimation.start()
                }
            }
            onExited: {
                startAnimation.stop()
                backAnimation.start()
            }
        }
    }

    PropertyAnimation {
        id: startAnimation

        target: title
        property: "contentX"
        to: title.contentWidth - title.width
        duration: {
            if (title.contentWidth > title.width) {
                return ((title.contentWidth - title.contentX) - title.width) * 6
            } else {
                return 0
            }
        }
    }

    PropertyAnimation {
        id: backAnimation

        target: title
        property: "contentX"
        to: 0
        duration: 300
    }
}

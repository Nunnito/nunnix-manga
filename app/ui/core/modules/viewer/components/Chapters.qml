import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../components" as C


C.ItemDelegate {
    width: listView.width
    height: 64

    rightPadding: 40

    C.CursorShape {cursorShape: Qt.PointingHandCursor}

    // Custom content
    contentItem: Item {
        width: parent.width

        // Chapter title
        C.Label {
            anchors.top: parent.top
            leftPadding: 25
            topPadding: 2

            text: modelData.title
            font.pixelSize: 14
        }
        // Chapter date and scanlation
        C.Label {
            anchors.bottom: parent.bottom
            leftPadding: 25
            bottomPadding: 2

            text: modelData.date + (modelData.scanlation ?
                            " • " + modelData.scanlation : "")
        }
    }
}

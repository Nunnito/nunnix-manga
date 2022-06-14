import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../components" as C
import "top-bar"


C.ItemDelegate {
    id: chapterDelegate

    width: listView.width
    height: 64

    rightPadding: 40
    highlighted: modelData.selected


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

    OpacityAnimator {
        target: chapterDelegate
        from: 0; to: 1
        duration: 500
        easing.type: Easing.InQuart
        running: _data && !completedAnims ? true : false
    }

    // MouseArea to select chapter with ctrl+click
    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onPressed: {
            // If right button is clicked, open context menu
            if (mouse.button == Qt.RightButton) {
                loader.active = true
            }

            if ((mouse.button == Qt.LeftButton) &&
                    (mouse.modifiers & Qt.ControlModifier ||
                        _data.chapters_data.selected_length > 0)) {
                modelData.selected = !modelData.selected
            } else {
                mouse.accepted = false
            }
        }
    }

    Loader {
        id: loader
        active: false
        source: "ChaptersContextMenu.qml"
    }
}

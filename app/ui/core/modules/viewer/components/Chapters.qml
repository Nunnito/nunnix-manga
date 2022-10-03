import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../components" as C
import "../../../../utils" as U
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

        // Chapter title row, with bookmark icon
        Row {
            leftPadding: modelData.bookmarked ? 20 : 25
            spacing: 5

            Image {
                sourceSize.width: 24
                sourceSize.height: 24

                source: Icon.get_icon("bookmark_filled.svg")
                visible: modelData.bookmarked
                U.ChangeColor {color: theme.windowAccent}  // Accent color
            }
            C.Label {
                id: title

                anchors.top: parent.top
                topPadding: 2

                text: modelData.title
                font.pixelSize: 14
                color: modelData.read ? theme.textfieldDecorationInactive :
                    modelData.bookmarked ? theme.windowAccent : theme.windowFg
            }
        }
        // Chapter date and scanlation
        C.Label {
            anchors.bottom: parent.bottom
            leftPadding: 25
            bottomPadding: 2

            text: modelData.date + (modelData.scanlation ?
                            " • " + modelData.scanlation : "")
            color: modelData.read ? theme.textfieldDecorationInactive :
                   modelData.bookmarked ? theme.windowAccent : theme.windowFg
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

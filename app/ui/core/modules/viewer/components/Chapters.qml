import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../../components" as C
import "top-bar"


C.ItemDelegate {
    property bool selected
    id: chapterDelegate

    width: listView.width
    height: 64

    rightPadding: 40
    highlighted: selected


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

        onPressed: {
            if ((mouse.button == Qt.LeftButton) && (mouse.modifiers & Qt.ControlModifier)) {
                selected = !selected
                if (!(topBar.tbStackView.currentItem.name == "selection")) {
                    topBar.tbStackView.push("top-bar/Selection.qml")
                }
            } else {
                mouse.accepted = false
            }
        }
    }
}

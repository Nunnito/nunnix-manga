import QtQuick 2.15
import QtQuick.Controls 2.15

import "../../../components" as C

C.Button {
    id: mangaSearchButton
    width: 140
    height: 210

    // Manga image
    Image {
        id: mangaCover
        anchors.fill: parent
        mipmap: true
        source: cover  // Manga cover from ListModel
        fillMode: Image.PreserveAspectCrop  // Crop the image
        opacity: 0

        OpacityAnimator {
            id: opacityAnimator
            target: mangaCover
            duration: 250
            easing.type: Easing.InQuart
            from: 0
            to: 1
        }

        // If the image is loaded, run the animation
		onStatusChanged: {
			if (status == 1) {
				opacityAnimator.start()
			}
		}
        // Background gradient for label.
        Rectangle {
            id: labelBackground

            width: parent.width
            height: parent.height

            // Text under the tile.
            C.Label {
                id: label

                bottomPadding: 5
                anchors.bottom: parent.bottom
                horizontalAlignment: Text.AlignHCenter

                width: mangaSearchButton.width

                text: title  // Manga title from ListModel
                font.pixelSize: 14
                elide: Text.ElideMiddle

            }

            // Gradient.
            gradient: Gradient {
                GradientStop { position: 0.6; color: "#00000000"}
                GradientStop { position: 0.9; color: "#CC000000"}
                GradientStop { position: 1.0; color: "#121212"}
            }
        }
    }

	C.BusyIndicator {
		id: busyIndicator

		anchors.centerIn: parent
	    running: mangaCover.status != 1  // Run if image is not loaded.
	}

	MouseArea {
		id: mouseArea

		// Manga tile tooltip. Appears when the mouse is over it for 1000 ms.
		ToolTip {
			id: tooltip
			visible: parent.containsMouse

			delay: 1000
			timeout: 5000

			C.Label {
				id: tooltipLabel

				text: label.text
				font.pixelSize: 14
			}
			background: Rectangle {
				color: theme.controlBg
                radius: 2
			}
		}
		hoverEnabled: true
		onPressed: mouse.accepted = false

		anchors.fill: parent
		cursorShape: Qt.PointingHandCursor
	}
}

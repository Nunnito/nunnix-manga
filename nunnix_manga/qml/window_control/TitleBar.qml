import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
	id: titleBar

	// Properties
	width: parent.width
	height: 24
	color: "#3A4047"

	// Rectangle button
	Component {
		id: rectangleButton

		Rectangle {
			id: button
			property string name

			height: titleBar.height
			width: titleBar.height

			color: mouseArea.containsMouse ? "#4C535B" : "#3A4047"

			// Icon button
			Image {
				id: image
				anchors.centerIn: parent
				source: {
					if (name == "close") {
						return "../resources/close.svg"
					}
					else if (name == "maximize") {
						return visibility == 4 ? "../resources/restore.svg" : "../resources/maximize.svg"
					}
					else {
						return "../resources/minimize.svg"
					}
				}
			}

			// Mouse events
			MouseArea {
				id: mouseArea
				anchors.fill: parent
				hoverEnabled: true

				onClicked: {
					if (name == "close") {
						close()
					}
					else if (name == "maximize") {
						visibility == 2 ? showMaximized() : showNormal()
					}
					else {
						showMinimized()
					}
				}
			}
		}
	}

	// Row that contains all action buttons
	Row {
		anchors.right: parent.right
		anchors.verticalCenter: parent.verticalCenter

		layoutDirection: Qt.RightToLeft
		height: titleBar.height

		Loader {
			sourceComponent: rectangleButton
			Component.onCompleted: item.name = "close"
		}
		Loader {
			sourceComponent: rectangleButton
			Component.onCompleted: item.name = "maximize"
		}
		Loader {
			sourceComponent: rectangleButton
			Component.onCompleted: item.name = "minimize"
		}
	}

	// Handler that allows to move the application.
	DragHandler {
		target: null
		grabPermissions: PointerHandler.TakeOverForbidden
		onActiveChanged: if (active) { rootWindow.startSystemMove()}
	}

	// Tap handler that allows double click to toggle maximize/restore.
	TapHandler {
		onDoubleTapped: visibility == 2 ? showMaximized() : showNormal()
	}
}

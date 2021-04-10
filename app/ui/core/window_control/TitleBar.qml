import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../utils"

Rectangle {
	id: titleBar

	// Properties
	width: parent.width
	height: 24
	color: theme.titleBg

	// Rectangle button
	Component {
		id: rectangleButton

		Rectangle {
			id: button
			property string name  // Possible names: close, maximize, minimize

			height: titleBar.height
			width: titleBar.height

			color: {
				if (mouseArea.containsMouse) {
					return name == "close" ? theme.titleButtonCloseBgOver
										   : theme.titleButtonBgOver
				}
				else {
					return name == "close" ? theme.titleButtonCloseBg
										   : theme.titleButtonBg
				}
			}

			// Icon button
			Image {
				id: image
				anchors.centerIn: parent
				source: {
					if (name == "close") {
						return Icon.get_icon("close.svg")
					}
					else if (name == "maximize") {
						return visibility == 4 ? Icon.get_icon("restore.svg")
											   : Icon.get_icon("maximize.svg")
					}
					else {
						return Icon.get_icon("minimize.svg")
					}
				}
				ChangeColor {
					color: {
						if (mouseArea.containsMouse) {
							return name == "close" ? theme.titleButtonCloseFgOver 
												   : theme.titleButtonFgOver
						}
						else {
							return name == "close" ? theme.titleButtonCloseFg
												   : theme.titleButtonFg
						}
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

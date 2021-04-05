import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Window 2.15

import "window_control"
import "theme"


ApplicationWindow {
    id: rootWindow

    visible: true

    // Minimum and initial width and height
	minimumWidth: Screen.width / 1.5
	minimumHeight: Screen.height / 1.5
    title: "Nunnix Manga"

	Material.theme:  Material.Dark
	flags: Qt.FramelessWindowHint | Qt.Window

	// Create the title bar and resize border
	menuBar: TitleBar {id: titleBar}
    ResizeBorder {}

	// instantiate theme colors
	Theme {id: t}
}

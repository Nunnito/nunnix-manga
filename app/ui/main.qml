import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Window 2.15

import "window_control"
import "theme"


ApplicationWindow {
    id: rootWindow

	// Is there a custom theme, load it, else load dark or light theme
	property var theme: Object.keys(thm).length ? thm : Material.theme ? Dark : Light

    // Minimum and initial width and height
	minimumWidth: Screen.width / 1.5
	minimumHeight: Screen.height / 1.5

	// Properties
    title: "Nunnix Manga"
    visible: true
	flags: Qt.FramelessWindowHint | Qt.Window

	// Material properties
	Material.theme:  Material.Dark

	// Create the title bar and resize border
	menuBar: TitleBar {id: titleBar}
    ResizeBorder {}
}

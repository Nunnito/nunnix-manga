import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Window 2.15

import "theme"
import "core"
import "core/window_control"


ApplicationWindow {
    id: rootWindow

	// Is there a custom theme, load it, else load dark or light theme
	property var theme: (Object.keys(themeConf).length ?
						 themeConf : Material.theme ? Dark : Light)

    // Minimum and initial width and height
	minimumWidth: Screen.width / 1.5
	minimumHeight: Screen.height / 1.5

	// Properties
    title: "Nunnix Manga"
    visible: true
	flags: Qt.FramelessWindowHint | Qt.Window

	// Material properties
	Material.theme: Material.Dark
	Material.accent: theme.windowAccent
 	Material.background: "#00000000"  // Fake background, for transparent borders
	Material.foreground: theme.windowFg

	// Create main UI and resize border
    ResizeBorder {}
	MainUI {id: mainUI}
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Window 2.15

import "sidebar"
import "window_control"


// This contains the main 
Page {
    property alias stackView: stackView
 	Material.background: theme.windowBg  // Real background

    // Set margins for resize border
    anchors.fill: parent
    anchors.margins: visibility === Window.Windowed ? 5 : 0

	// Create the title bar and resize border
    header: TitleBar {id: titleBar}

    Row {
        property alias stackView: stackView 
        anchors.fill: parent

        SideBar {id: sideBar}

        StackView {
            id: stackView
            implicitWidth: sideBar.visible ? parent.width - sideBar.width : parent.width
            implicitHeight: parent.height
            initialItem: "library/Library.qml"
        }
    }
}


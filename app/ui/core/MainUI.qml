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

        SideBar {id: sideBar; z: 99}

        StackView {
            id: stackView
            implicitWidth: sideBar.visible ?
                           parent.width - sideBar.width : parent.width
            implicitHeight: parent.height
            initialItem: "modules/library/Library.qml"

            replaceEnter: Transition {
                OpacityAnimator {from: 0; to: 1; duration: 250}
            }
            replaceExit: Transition {
                OpacityAnimator {from: 1; to: 0; duration: 250}
            }
        }
    }
}


import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../components" as C

// Sidebar custom button
C.ItemDelegate {
    property string target        // Target name
    property string targetPath    // Target relative path
    property string iconFilled    // Icon-filled name
    property string iconOutlined  // Icon-outlined name

    Layout.preferredWidth: sideBar.width
    Layout.preferredHeight: sideBar.width

    colorBg: theme.sidebarButtonBg
    colorFg: theme.sidebarButtonFg
    colorBgOver: theme.sidebarButtonBgOver
    colorFgOver: theme.sidebarButtonFgOver

    highlighted: (stackView.currentItem.name == target) ? true : false
    display: AbstractButton.IconOnly

    firstIcon.icon.source: Icon.get_icon(iconOutlined)
    secondIcon.icon.source: Icon.get_icon(iconFilled)

    onClicked: {
        if (!highlighted) {
            stackView.replace(targetPath)
        }
    }    
}

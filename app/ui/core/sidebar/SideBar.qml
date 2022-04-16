import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

import "../../components" as C
import "components"


// Sidebar UI
Rectangle {
    id: sideBar

    width: 56
    height: parent.height

    color: theme.sidebarBg

    // Pane for elevation shadow
    Pane {
        anchors.fill: parent
        Material.background: parent.color
        Material.elevation: 9
    }

    // Positionate all buttons
    ColumnLayout {
        height: sideBar.height
        spacing: 0

        LibraryButton {}
        ExploreButton {}
        DownloadsButton {}
        HistoryButton {}
        C.Spacer {}
        SettingsButton {}
    }
}

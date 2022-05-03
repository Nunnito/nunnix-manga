import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../components" as C

// Use topbar as status bar
C.TopBar {
    height: 30
    RowLayout {
        width: parent.width
        height: parent.height
        layoutDirection: Qt.RightToLeft 
        spacing: 0

        C.ComboBox {
            colorBg: theme.topBarBg  // Set same color as top bar

            Layout.preferredWidth: 128
            Layout.preferredHeight: parent.height

            model: Explorer.scrapers_list  // Scrapers list
            indicator: null  // no dropdown arrow
            flat: true

            topInset: 0
            bottomInset: 0
        }
    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C

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

            C.CursorShape {cursorShape: Qt.PointingHandCursor}

            onActivated: {
                model = Explorer.scrapers_list  // Set scrapers list
                Explorer.scraper = currentText  // Set scraper

                // Set visibility of advanced search
                if (Explorer.advanced_search) {
                    explorer.topBar.advancedSearchButton.visible = true
                } else {
                    explorer.topBar.advancedSearchButton.visible = false
                }

                // Set new advanced search controls
                explorer.advancedSearch.controls.model = Explorer.advanced_search

                explorer.searchModel.clear()  // Clear search results
                explorer.currentPage = 1  // Reset page to 1
                explorer.searchType = "empty"  // Reset search type to empty
                
                Explorer.search(explorer.searchType, explorer,
                                    explorer.currentPage)  // Do search
            }
        }
    }
}

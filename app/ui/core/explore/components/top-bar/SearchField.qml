import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C


C.TextField {
    Layout.fillWidth: true
    Layout.leftMargin: 20
    Layout.rightMargin: 20

    placeholderText: qsTr("Search")

    onAccepted: {
        explorer.searchModel.clear()  // Clear search results
        explorer.currentPage = 1  // Reset page to 1
        explorer.searchType = text ? "title" : "empty"

        // Do search
        Explorer.search_manga(explorer.searchType, this, explorer.currentPage)
    }
}

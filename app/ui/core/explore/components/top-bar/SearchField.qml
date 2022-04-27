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
        // If text not is empty, // Set search text as title
        if (text) {
            explorer.searchParams["title"] = text
        }
        // Else, remove search key from params
        else {
            delete explorer.searchParams["title"]
        }
        explorer.searchModel.clear()  // Clear search results
        explorer.searchParams["page"] = 1  // Reset page to 1
        Explorer.search_manga(explorer.searchParams)
    }
}

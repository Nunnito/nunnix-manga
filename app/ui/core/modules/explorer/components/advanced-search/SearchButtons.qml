import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import "../../../../../components" as C

// This is the bottom bar that displays "SEARCH" and "RESET" buttons
Pane {
    property alias searchButton: searchButton

    width: parent.width + advancedSearch.leftPadding * 2
    height: 48 + (advancedSearch.leftPadding / 2)

    y: parent.height - height + advancedSearch.leftPadding
    x: -advancedSearch.leftPadding

    Material.elevation: 3
    Material.background: theme.advancedSearchSearchBg2

    Row {
        width: listView.width
        anchors.verticalCenter: parent.verticalCenter

        spacing: 10
        x: advancedSearch.leftPadding - 10
        
        C.Button {
            id: searchButton

            highlighted: true
            width: parent.width / 2 - spacing

            text: qsTr("Search")

            C.CursorShape {cursorShape: Qt.PointingHandCursor}

            contentItem: C.Label {
                text: parent.text  
                color: theme.windowBg
                font.bold: true
                font.capitalization: Font.AllUppercase

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            onClicked: {
                explorer.searchModel.clear()  // Clear search results
                explorer.currentPage = 1  // Reset page to 1
                explorer.searchType = "advanced"
                Explorer.search(explorer.searchType, explorer,
                                      explorer.currentPage)
            }
        }

        C.Button {
            width: parent.width / 2 - spacing
            text: qsTr("RESET")
            flat: true
            highlighted: true

            C.CursorShape {cursorShape: Qt.PointingHandCursor}

            onClicked: {
                listView.model = null
                listView.model = Explorer.advanced_search
            }
        }
    }
}

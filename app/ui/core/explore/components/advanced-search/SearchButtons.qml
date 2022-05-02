import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import "../../../../components" as C

// This is the bottom bar that displays "SEARCH" and "RESET" buttons
Pane {
    width: parent.width + advancedSearch.leftPadding * 2
    height: 48 + (advancedSearch.leftPadding / 2)

    y: parent.height - height + advancedSearch.leftPadding
    x: -advancedSearch.leftPadding

    Material.elevation: 3
    Material.background: theme.advancedSearchSearchBg2

    Row {
        width: listView.width
        anchors.verticalCenter: parent.verticalCenter

        spacing: 5
        x: advancedSearch.leftPadding
        
        C.Button {
            highlighted: true
            width: parent.width / 2 - spacing
            colorBgOver: theme.advancedSearchSearchButtonBgOver

            text: qsTr("Search")

            contentItem: C.Label {
                text: parent.text  
                color: theme.windowBg
                font.bold: true
                font.capitalization: Font.AllUppercase

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        C.Button {
            width: parent.width / 2 - parent.spacing
            text: qsTr("RESET")
            flat: true
            highlighted: true
        }
    }
}

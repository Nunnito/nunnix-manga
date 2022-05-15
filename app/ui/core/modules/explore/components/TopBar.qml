import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C
import "top-bar"

C.TopBar {
    property alias searchField: searchField
    property alias searchButton: searchButton
    property alias advancedSearchButton: advancedSearchButton

    RowLayout {
        width: parent.width
        spacing: 0

        SearchField {id: searchField}
        SearchButton {id: searchButton}
        AdvancedSearchButton {id: advancedSearchButton}
    }
}

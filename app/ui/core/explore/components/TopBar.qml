import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../components" as C
import "top-bar"

C.TopBar {
    RowLayout {
        width: parent.width
        spacing: 0

        SearchField {}
        SearchButton {}
        MenuButton {}
    }
}

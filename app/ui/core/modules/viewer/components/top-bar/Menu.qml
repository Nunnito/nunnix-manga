import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "menu"

RowLayout {
    property string name: "menu"

    width: topBar.width
    spacing: 0

    BackButton {}
    C.Spacer {orientation: "horizontal"}
    BookmarkButton {}
    DownloadButton {visible: false}
    MenuButton {}
}

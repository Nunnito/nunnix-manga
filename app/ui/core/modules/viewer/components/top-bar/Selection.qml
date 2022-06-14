import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "selection"

RowLayout {
    property string name: "selection"

    width: topBar.width
    spacing: 10

    DownloadButton {Layout.leftMargin: 10; visible: false}
    BookmarkButton {Layout.leftMargin: 10}
    MarkAsReadButton {}
    C.Spacer {orientation: "horizontal"}
    SelectAllButton {}
    CancelButton {Layout.rightMargin: 10}
}

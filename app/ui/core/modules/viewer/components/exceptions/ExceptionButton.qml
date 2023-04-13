import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../../components" as C

C.RoundButton {
    text: qsTr("Retry")
    flat: true
    icon.source: Icon.get_icon("refresh.svg")
    display: AbstractButton.TextUnderIcon
    width: height * 2
    height: icon.height * 3
    anchors.horizontalCenter: parent.horizontalCenter

    onClicked: {
        _data ? _data.reload() : getData()
        _data = null, _chapters = null
        listView.headerItem.filterChapters.height = 0
        listView.headerItem.filterChapters.opacity = 0
    }
}

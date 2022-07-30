import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


C.RoundButton {
    flat: true
    icon.source: Icon.get_icon("filter-list.svg")

    Layout.rightMargin: 20
    C.CursorShape {cursorShape: Qt.PointingHandCursor}
}

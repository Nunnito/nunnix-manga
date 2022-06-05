import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


Column {
    C.Label {
        text: qsTr("Genres")
        font.bold: true
        font.pixelSize: 14
    }

    ListView {
        width: _header.width - (image.width + (row.padding * 2))
        height: 40

        clip: true
        spacing: 5

        interactive: false
        boundsMovement: GridView.StopAtBounds
        orientation: ListView.Horizontal

        model: _data ? _data.genres : null
        delegate: C.RoundButton {
            text: _data.genres[index]
            leftInset: 0
            rightInset: 0
            C.CursorShape {cursorShape: Qt.PointingHandCursor}
        }

        ScrollBar.horizontal: C.ScrollBar {height: 10}
        U.WheelArea {horizontalScrolling: true}
    }
}

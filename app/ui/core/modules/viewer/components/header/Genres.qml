import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U


Column {
    C.Label {
        id: label

        text: qsTr("Genres")
        font.bold: true
        font.pixelSize: 14
        visible: _data ? true : false
    }

    ListView {
        id: genres

        width: _header.width - (image.width + (row.padding * 2))
        height: 40

        clip: true
        spacing: 5
        visible: _data ? true : false

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
        header: C.Label {
            width: 0
            text: qsTr("No genres available")
            visible: _data ? _data.genres.length == 0 : false
        }

        ScrollBar.horizontal: C.ScrollBar {height: 10}
        U.WheelArea {horizontalScrolling: true}
    }

    // Rectangle placeholder when no data is available
    LoaderPlaceHolder {height: genres.height + label.height; width: genres.width}
}

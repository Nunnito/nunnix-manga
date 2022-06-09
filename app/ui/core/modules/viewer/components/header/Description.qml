import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../../components" as C
import "../../../../../utils" as U

Column {
    C.Label {
        id: label

        text: qsTr("Description")
        font.bold: true
        font.pixelSize: 14
        visible: _data ? true : false
    }

    Flickable {
        id: flickable

        width: _header.width - (image.width + (row.padding * 2))
        height: background.height - (parent.y + row.padding * 2 + row.spacing * 4)

        clip: true
        contentHeight: description.height

        boundsMovement: Flickable.StopAtBounds
        interactive: false
        visible: _data ? true : false

        C.Label {
            id: description

            width: _header.width - (image.width + (row.padding * 2) + scrollBar.width)
            text: _data ? (_data.description ? _data.description :
                           qsTr("No description available.")) : ""
            wrapMode: Label.WordWrap
            font.pixelSize: 14
        }

        ScrollBar.vertical: C.ScrollBar {
            id: scrollBar
            width: 10
            policy: flickable.height > flickable.contentHeight ?
                                       ScrollBar.AsNeeded : ScrollBar.AlwaysOn
        }
        U.WheelArea {parent: flickable}
    }

    // Rectangle placeholder when no data is available
    LoaderPlaceHolder {height: flickable.height + description.height; width: description.width}
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../../../../components" as C
import "header" as H

Item {
    id: _header

    width: parent.width
    height: background.height

    H.Background {id: background}
    Column {
        id: column
        width: parent.width

        Row {
            id: row

            padding: 40
            spacing: 20

            H.Image {id: image}
            Column {
                spacing: row.spacing

                H.Title {}
                Column {
                    spacing: _data ? 0 : 6
                    H.Author {}
                    H.Status {}
                }
                H.Genres {}
                H.Description {}
            }
        }
        H.TotalChapters {}
    }
}

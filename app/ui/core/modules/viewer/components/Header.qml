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

                H.Title {id: title}
                Column {
                    spacing: _data ? 0 : 6
                    H.Author {id: author}
                    H.Status {id: status}
                }
                H.Genres {id: genres}
                H.Description {id: description}
            }
        }
        RowLayout {
            width: column.width
            H.TotalChapters {id: totalChapters}
            C.Spacer {orientation: "horizontal"}
            H.FilterChapters {id: filterChapters}
        }
    }

    // Opacity animation
    PropertyAnimation {
        targets: [title, author, status, genres, description, totalChapters]
        properties: "opacity"
        from: 0; to: 1
        duration: 500
        running: _data ? true : false
        easing.type: Easing.InQuart

        onFinished: completedAnims = true
    }
}

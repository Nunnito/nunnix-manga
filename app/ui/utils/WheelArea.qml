import QtQuick 2.15

// TODO: Several improvements, redo the whole thing
MouseArea {
    property bool useContentX: false

    property real toContentY: 0

    id: mouseArea

    z: -1
    width: parent.width
    height: parent.height

    onWheel: {
        var mouseMove = wheel.angleDelta.y % 120 == 0 ? wheel.angleDelta.y : wheel.angleDelta.y / 4

        if (contentYAnimation.running) {
            contentYAnimation.stop()
            toContentY -= mouseMove
            if (toContentY > (parent.contentHeight - parent.height) + parent.bottomMargin ){
                toContentY = (parent.contentHeight - parent.height) + parent.bottomMargin
            }
            else if (toContentY < -parent.topMargin) {
                toContentY = -parent.topMargin
            }

        }
        else {
            toContentY = parent.contentY - mouseMove
            if (toContentY > (parent.contentHeight - parent.height) + parent.bottomMargin ){
                toContentY = (parent.contentHeight - parent.height) + parent.bottomMargin
            }
            else if (toContentY < -parent.topMargin) {
                toContentY = -parent.topMargin
            }
        }
        if (mouseMove == wheel.angleDelta.y) {
            contentYAnimation.duration = 500
        }
        else {
            contentYAnimation.duration = 250
        }
        contentYAnimation.start()
    }

    PropertyAnimation {
        id: contentYAnimation
        property: "contentY"

        easing.type: Easing.OutQuad
        target: parent
        to: toContentY
    }
}

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
        var mouseMove = wheel.angleDelta.y % 120 == 0 ? wheel.angleDelta.y :
                                                        wheel.angleDelta.y / 4
        if (parent.atYEnd || parent.atYBeginning) {
            contentYAnimation.stop()
        }

        if (contentYAnimation.running) {
            contentYAnimation.stop()
            toContentY -= mouseMove
        }
        else {
            toContentY = parent.contentY - mouseMove
        }

        let touchpadDuration = Math.round(Math.abs(parent.contentY - toContentY))
        contentYAnimation.duration = wheel.angleDelta.y % 120 == 0 ? 500 :
                                                                     touchpadDuration
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

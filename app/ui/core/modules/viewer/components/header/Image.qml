import QtQuick 2.15
import QtQuick.Controls 2.15

// Manga image
Rectangle {
    width: 210
    height: 315

    color: theme.controlBg

    Image {
        id: image

        width: parent.width
        height: parent.height

        source: _data ? _data.cover : ""
        fillMode: Image.PreserveAspectCrop

        
        BusyIndicator {
            anchors.centerIn: parent
            running: image.status == 1 ? 0:1
        }

        OpacityAnimator {
            id: opacityAnim
            target: image
            from: 0; to: 1
            duration: 500
            easing.type: Easing.InQuart
            running: image.status == 1 ? 1:0
        }

        onStatusChanged: {
            if (status == 3) {  // Retry if loading failed
                source = ""
                source = _data.cover
            }
        }
    }
}

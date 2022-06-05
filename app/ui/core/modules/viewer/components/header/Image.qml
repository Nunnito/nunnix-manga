import QtQuick 2.15
import QtQuick.Controls 2.15

// Manga image
Image {
    id: image

    width: 210
    height: 315

    source: _data ? _data.cover : ""
    fillMode: Image.PreserveAspectCrop

    
    Rectangle {
        anchors.fill: parent
        color: theme.controlBg
        visible: image.status == 1 ? 0:1
    }

    BusyIndicator {
        anchors.centerIn: parent
        running: image.status == 1 ? 0:1
    }

    OpacityAnimator {id: opacityAnim; target: image; from: 0; to: 1; duration: 500}

    onStatusChanged: {
        if (status == 1) {
            opacityAnim.start()
        } else if (status == 3) {  // Retry if loading failed
            source = ""
            source = _data.cover
        }
    }
}

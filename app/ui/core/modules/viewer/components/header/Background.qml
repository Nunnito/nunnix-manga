import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

// A blurry image
Item {
    width: parent.width
    height: 448
    
    Image {
        id: background

        width: parent.width
        height: parent.height

        asynchronous: true
        source: _data ? _data.cover : ""
        fillMode: Image.PreserveAspectCrop
        opacity: 0

        onStatusChanged: {
            if (status == 3) {  // Retry if loading failed
                source = ""
                source = _data.cover
            }
        }
    }

    Rectangle {
        id: gradient
        anchors.fill: background
        z: 1

        // Add a gradient to the image background
        gradient: Gradient {
            GradientStop {id: ano; position: 0.6; color: theme.topBarBg}
            GradientStop { position: 0.9; color: theme.windowBg}
            GradientStop { position: 1.0; color: theme.windowBg}
        }
    }

    // If there is no image
    Rectangle {
        anchors.fill: background
        visible: background.status == 1 ? 0:1
        z: 1

        gradient: Gradient {
            GradientStop { position: 0.6; color: theme.topBarBg}
            GradientStop { position: 0.9; color: theme.windowBg}
            GradientStop { position: 1.0; color: theme.windowBg}
        }
    }

    FastBlur {
        id: blur

        width: background.width
        height: background.height
        source: background
        radius: 32
    }

    OpacityAnimator {
        target: blur
        from: 0; to: 1
        duration: 500
        easing.type: Easing.InQuart
        running: background.status == 1 ? 1:0
    }

    PropertyAnimation {
        target: ano
        properties: "color"
        from: theme.topBarBg
        to: "#CC000000"
        duration: 500
        easing.type: Easing.InQuart
        running: background.status == 1 ? 1 : 0
    }
}

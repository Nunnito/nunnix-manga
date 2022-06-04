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

        source: _data ? _data.cover : ""
        fillMode: Image.PreserveAspectCrop
        
        Rectangle {
            anchors.fill: parent

            // Add a gradient to the image background
            gradient: Gradient {
                GradientStop { position: 0.6; color: "#CC000000"}
                GradientStop { position: 0.9; color: theme.windowBg}
                GradientStop { position: 1.0; color: theme.windowBg}
            }
        }

        // If there is no image
        Rectangle {
            anchors.fill: parent
            visible: background.status == 1 ? 0:1

            gradient: Gradient {
                GradientStop { position: 0.6; color: theme.topBarBg}
                GradientStop { position: 0.9; color: theme.windowBg}
                GradientStop { position: 1.0; color: theme.windowBg}
            }
        }

        onStatusChanged: {
            if (status == 1) {
                opacityAnim.start()
            } else if (status == 3) {  // Retry if loading failed
                source = ""
                source = _data.cover
            }
        }
    }

    FastBlur {
        width: background.width
        height: background.height
        source: background
        radius: 32
    }
    OpacityAnimator {id: opacityAnim; target: background; from: 0; to: 1; duration: 500}
}

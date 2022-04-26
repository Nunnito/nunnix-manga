import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    property int b: 5  // Border size
    anchors.fill: parent

    // This mouse area is only to change the cursor shape
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true

        cursorShape: {
            const p = Qt.point(mouseX, mouseY);  // Position

            if (p.x < b && p.y < b) return Qt.SizeFDiagCursor;
            if (p.x >= width - b && p.y >= height - b) return Qt.SizeFDiagCursor;
            if (p.x >= width - b && p.y < b) return Qt.SizeBDiagCursor;
            if (p.x < b && p.y >= height - b) return Qt.SizeBDiagCursor;
            if (p.x < b || p.x >= width - b) return Qt.SizeHorCursor;
            if (p.y < b || p.y >= height - b) return Qt.SizeVerCursor;
        }
        acceptedButtons: Qt.NoButton
    }

    // DragHandler to allow native resize
    DragHandler {
        id: resizeHandler
        target: null

        onActiveChanged: if (active) {
            const p = resizeHandler.centroid.scenePressPosition;  // Position
            let e = 0;  // Edges

            if (p.x < b) {e |= Qt.LeftEdge}
            if (p.x >= width - b) {e |= Qt.RightEdge}
            if (p.y < b) {e |= Qt.TopEdge}
            if (p.y >= height - b) {e |= Qt.BottomEdge}

            if (e != 0) rootWindow.startSystemResize(e);
        }
    }
}

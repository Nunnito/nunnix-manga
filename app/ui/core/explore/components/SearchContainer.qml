import QtQuick 2.15
import "../../../components" as C
import "../../../utils" as U


GridView {
    property int spacing: 20
    property int columns: Math.floor((width - (rightMargin + leftMargin)) / 160)
    
    width: parent.width
    height: parent.height - topBar.height
    cellWidth: 160
    cellHeight: 250
    
    interactive: false
    delegate: ContentTile {}
    clip: true
    model: searchModel  // searchModel, from parent

    rightMargin: 20
    leftMargin: 20
    topMargin: 50
    bottomMargin: 50

    x: ((width - (columns * cellWidth)) / 2) - 10

    populate: Transition {
        OpacityAnimator {from: 0; to: 1; duration: 500}
    }

    // Appears in a new search.
    C.BusyIndicator {
        id: busyIndicator
        x: (parent.width - (width + parent.x * 2)) / 2
        y: (parent.height - height - 100) / 2

        running: parent.count == 0
    }

    U.WheelArea {
        width: parent.width - parent.x
    }

    // When end is reached, load more.
    onAtYEndChanged: {
        if (atYEnd && count > 0) {  // If we're at the end and there are items
            parent.searchParams["page"]++  // Increment the page
            Explorer.search_manga(parent.searchParams)
        }
    }
}

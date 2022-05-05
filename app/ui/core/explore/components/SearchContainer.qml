import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../components" as C
import "../../../utils" as U


GridView {
    property int spacing: 20
    property int columns: Math.floor((width - (rightMargin + leftMargin)) / 160)
    
    width: parent.width
    height: parent.height - topBar.height - statusBar.height
    cellWidth: 160
    cellHeight: 250
    z: -1
    
    interactive: false
    delegate: ContentTile {}
    boundsMovement: GridView.StopAtBounds
    model: searchModel  // searchModel, from parent

    rightMargin: 20
    leftMargin: 20
    topMargin: 50
    bottomMargin: 50

    x: ((width - (columns * cellWidth)) / 2) - 10

    populate: Transition {
        OpacityAnimator {from: 0; to: 1; duration: 500}
    }
    add: Transition {
        OpacityAnimator {from: 0; to: 1; duration: 500}
    }
    remove: Transition {
        OpacityAnimator {from: 1; to: 0; duration: 250}
    }

    footer: explorer.endOfResults ? endOfResultsLabel : moreResultsBusyIndicator 

    ScrollBar.vertical: C.ScrollBar {
        visible: explorer.advancedSearch.width == 300 || explorer.advancedSearch.width == 0
        x: size >= 1 ? 0 : parent.width - (parent.x + width)
    }

    // Appears in a new search.
    C.BusyIndicator {
        id: busyIndicator
        x: (parent.width - (width + parent.x * 2)) / 2
        y: (parent.height - height) / 2
        z: -1

        running: parent.count == 0 && !noResults && !endOfResults &&
                 !connectionError && !timeOutError && !unknownError
    }

    // Appears if there are no results.
    C.Label {
        id: noResultsLabel
        text: qsTr("No results found")
        font.bold: true
        font.pixelSize: 21
        visible: explorer.noResults

        x: (parent.width - (width + parent.x * 2)) / 2
        y: (parent.height - height) / 2
        z: -1
    }

    // Appears when no more results are found (footer).
    Component {
        id: endOfResultsLabel
        C.Label {
            text: qsTr("End of results.")
            font.bold: true
            font.pixelSize: 14

            width: (columns * cellWidth) - contentHeight
            horizontalAlignment: Text.AlignHCenter
            
            visible: explorer.endOfResults
            z: -1
        }
    }

    // Appears when is loading more results (footer).
    Component {
        id: moreResultsBusyIndicator
        C.BusyIndicator {
            width: busyIndicator.x * 2 + 15
            running: explorer.grid.count > 0 && !explorer.endOfResults
            z: -1
        }
    }

    // Custom mouse wheel event.
    U.WheelArea {
        width: parent.width - parent.x
    }

    // When end is reached, load more.
    onAtYEndChanged: {
        // If we're at the end and there are items to load, load more.
        if (atYEnd && count > 0 && !endOfResults) {
            explorer.currentPage++  // Increment the page
            Explorer.search_manga(explorer.searchType,
                                  explorer,
                                  explorer.currentPage)
        }
    }
    onCountChanged: {
        // If we're at the end and there are items to load, load more.
        if (atYEnd && count > 0 && !endOfResults) {
            explorer.currentPage++  // Increment the page
            Explorer.search_manga(explorer.searchType,
                                  explorer,
                                  explorer.currentPage)
        }
    }
}

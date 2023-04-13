import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C
import "../../../../utils" as U


GridView {
    property int spacing: 20
    property int columns: Math.floor((width - (rightMargin + leftMargin)) / 160)

    id: gridView
    
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

    footer: explorer.endOfResults ? endOfResultsLabel 
            : explorer.connectionError || explorer.timeOutError || explorer.unknownError
            ? connectionErrorFooter : moreResultsBusyIndicator 

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

        running: parent.count == 0 && !explorer.noResults &&
                 !explorer.endOfResults && !explorer.connectionError &&
                 !explorer.timeOutError && !explorer.unknownError
    }

    // Appears if there are no results.
    C.Label {
        id: noResultsLabel
        text: qsTr("No results found")
        font.bold: true
        font.pixelSize: 18
        visible: explorer.noResults

        x: (parent.width - (width + parent.x * 2)) / 2
        y: (parent.height - height) / 2
        z: -1
    }

    // Appears if there are a connection, timeout error or an unknown error.
    Column {
        id: connectionErrorLabel
        width: parent.width
        y: (gridView.height - height) / 2
        visible: (explorer.connectionError || explorer.timeOutError ||
                  explorer.unknownError) && gridView.count == 0

        C.Label {
            text: explorer.connectionError ? qsTr("Connection error")
                  : explorer.timeOutError ? qsTr("Time out")
                  : explorer.errorMessage
            font.bold: true
            font.pixelSize: 18
            x: (gridView.width - (width + gridView.x * 2)) / 2
        }
        Column {
            C.RoundButton {
                text: qsTr("Retry")
                flat: true
                icon.source: Icon.get_icon("refresh.svg")
                width: height * 2
                height: icon.height * 3
                display: AbstractButton.TextUnderIcon
                x: (gridView.width - (width + gridView.x * 2)) / 2

                onClicked: Explorer.search(explorer.searchType, explorer,
                                                 explorer.currentPage)
            }
        }
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

    // Appears if there are a connection, timeout error or an unknown error (footer).
    Component {
        id: connectionErrorFooter
        Column {
            width: gridView.width
            y: (gridView.height - height) / 2
            visible: (explorer.connectionError || explorer.timeOutError
                      || explorer.unknownError) && explorer.grid.count > 0

            C.Label {
                text: explorer.connectionError ? qsTr("Connection error")
                       : explorer.timeOutError ? qsTr("Time out")
                       : explorer.errorMessage
                font.bold: true
                font.pixelSize: 14
                x: (gridView.width - (width + gridView.x * 2)) / 2
            }
            Column {
                C.RoundButton {
                    text: qsTr("Retry")
                    flat: true
                    icon.source: Icon.get_icon("refresh.svg")
                    width: height * 2
                    height: icon.height * 3
                    display: AbstractButton.TextUnderIcon
                    x: (gridView.width - (width + gridView.x * 2)) / 2

                    onClicked: Explorer.search(explorer.searchType,
                                                     explorer,
                                                     explorer.currentPage)
                }
            }
        }
    }

    // Custom mouse wheel event.
    U.WheelArea {
        width: parent.width - parent.x
    }

    // When end is reached, load more.
    onAtYEndChanged: {
        // If we're at the end and there are items to load, load more.
        if (atYEnd && count > 0 && !explorer.noResults &&
            !explorer.endOfResults && !explorer.connectionError &&
            !explorer.timeOutError && !explorer.unknownError) {
            explorer.currentPage++  // Increment the page
            Explorer.search(explorer.searchType,
                                  explorer,
                                  explorer.currentPage)
        }
    }
    onCountChanged: {
        // If we're at the end and there are items to load, load more.
        if (atYEnd && count > 0 && !explorer.noResults &&
            !explorer.endOfResults && !explorer.connectionError &&
            !explorer.timeOutError && !explorer.unknownError) {
            explorer.currentPage++  // Increment the page
            Explorer.search(explorer.searchType,
                                  explorer,
                                  explorer.currentPage)
        }
    }
}

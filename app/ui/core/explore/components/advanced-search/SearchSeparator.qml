import QtQuick 2.15
import QtQuick.Controls 2.15
import "../../../../components" as C

C.Separator {
    width: listView.width
    topPadding: modelData.topPadding ? modelData.topPadding : topPadding
    bottomPadding: modelData.bottomPadding ? modelData.bottomPadding : bottomPadding
}

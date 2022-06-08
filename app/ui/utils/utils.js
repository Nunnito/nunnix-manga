function copy(text) {
    var x = Qt.createQmlObject("import QtQuick 2.15; TextEdit{visible: false}", rootWindow)

    x.text = text
    x.selectAll()
    x.copy()
    x.destroy()
}

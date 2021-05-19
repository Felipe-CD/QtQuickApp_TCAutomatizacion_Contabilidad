import QtQuick 2.0
import QtQuick.Controls 2.15

Item {
    Rectangle {
        id: rectangle
        color: "#2c313c"
        anchors.fill: parent

        Rectangle {
            id: titleProgram
            height: 77
            color: "#5c667d"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: 40
            anchors.rightMargin: 40
            anchors.leftMargin: 40

            Label {
                id: label
                x: 341
                y: 32
                color: "#ffffff"
                text: qsTr("Automatización de busqueda en PayU y cruce con Querys")
                anchors.verticalCenter: parent.verticalCenter
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 18
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        Rectangle {
            id: textDescription
            color: "#1d2128"
            radius: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: titleProgram.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: 20
            anchors.rightMargin: 40
            anchors.leftMargin: 40
            anchors.bottomMargin: 40

            Label {
                id: label1
                x: 10
                y: 231
                color: "#a9b2c8"
                text: qsTr("Programa elaborado por Andrés Felipe Castillo
Para soporte contactar a: andres.castillod@claro.com.co - (+57) 312 396 3738
Versión 1.0
")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 11
                anchors.rightMargin: 3
                anchors.leftMargin: 0
                anchors.bottomMargin: 10
            }

            Text {
                id: text1
                color: "#838a9c"
                text: "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:6.6pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">El programa recibe un </span><span style=\" font-size:12pt; font-weight:600;\">libro de excel (.xlsx)</span><span style=\" font-size:12pt;\"> que contiene los registros para identificar<br />el número de cuenta que se encuentra en las bases mensuales transaccionales de PayU.<br />Luego busca estos registros identificados con su número de cuenta en las bases<br />mensuales de Querys para su respectivo cruce de valores. (El programa cruza hasta<br />diferencias de +-500).</span></p></body></html>"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: label1.top
                font.pixelSize: 15
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignTop
                anchors.bottomMargin: 10
                anchors.topMargin: 10
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                textFormat: Text.RichText
            }
        }
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.66;height:480;width:800}D{i:2}D{i:5}D{i:6}D{i:4}
}
##^##*/

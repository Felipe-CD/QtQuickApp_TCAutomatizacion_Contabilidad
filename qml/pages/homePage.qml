import QtQuick 2.0
import QtQuick.Controls 2.15
import "../controls"
import QtQuick.Layouts 1.0
import QtQuick.Dialogs 1.3

Item {
    id: item1
    property string setText: ""

    Rectangle {
        id: mainPage
        color: "#2c313c"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 0
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0

        Rectangle {
            id: rectabgleTop
            height: 60
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 30
            anchors.leftMargin: 30
            anchors.topMargin: 50

            GridLayout {
                anchors.fill: parent
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                anchors.bottomMargin: 10
                anchors.topMargin: 10
                rows: 1
                columns: 2

                CustomTextField{
                    id: selectedFile
                    height: 40
                    color: "#ffffff"
                    text: "Seleccione el archivo"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.NoWrap
                    Layout.preferredHeight: 40
                    font.pointSize: 12
                    Layout.fillWidth: true
                    Layout.preferredWidth: 469
                    textFormat: Text.PlainText
                }

                OpenBtn {
                    id: openbutton
                    Layout.fillWidth: true
                    Layout.preferredWidth: 212

                    onPressed: {
                        fileOpen.open()
                    }

                    FileDialog{
                        id: fileOpen
                        title: "Escoja el archivo"
                        folder: shortcuts.home
                        selectMultiple: false
                        nameFilters: ["Excel file (*.xlsx)"]
                        onAccepted: {
                            backend.openFile(fileOpen.fileUrl)
                        }

                    }
                }
            }
        }
        Rectangle{
            id: rectangleExecute
            height: 40
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rectabgleTop.bottom
            anchors.rightMargin: 34
            anchors.leftMargin: 30
            anchors.topMargin: 10

            ExecuteBtn{
                id: executeProgram
                height: 40
                anchors.left: parent.left
                anchors.right: parent.right
                textBtn: "EJECUTAR"
                colorDefault: "#177adb"
                anchors.rightMargin: 10
                anchors.leftMargin: 10
                onClicked: {
                    backend.start_worker()
                }

            }

        }

        ProgressBar {
            id: progressBar
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: rectangleExecute.bottom
            anchors.rightMargin: 60
            anchors.leftMargin: 60
            anchors.topMargin: 50
            padding: 0
            from: 0
            to: 100.0


            background: Rectangle {
                implicitWidth: 200
                implicitHeight: 16
                color: "#95969d"
                radius: 3
            }

            contentItem: Item {
                implicitWidth: 200
                implicitHeight: 14

                Rectangle {
                    width: progressBar.visualPosition * parent.width
                    height: parent.height
                    color: "#30cfd0"
                    radius: 2
                    gradient: Gradient {
                        GradientStop {
                            position: 0
                            color: "#243949"
                        }

                        GradientStop {
                            position: 1
                            color: "#177adb"
                        }
                    }
                }
            }
        }

        Flickable {
            id: flickable
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: progressBar.bottom
            anchors.bottom: parent.bottom
            anchors.topMargin: 30
            anchors.bottomMargin: 20
            anchors.rightMargin: 30
            anchors.leftMargin: 30

            TextArea.flickable: TextArea{
                id: textArea
                padding: 10
                textFormat: Text.AutoText
                selectedTextColor: "#ffffff"
                selectionColor: "#ff007f"
                color: "#ffffff"
                font.pointSize: 12
                text: setText
            }

            ScrollBar.vertical: ScrollBar{}
        }



    }

    Connections{
        target: backend

        function onNameFile(name){
            selectedFile.text = name
        }
        function onProgressChanged(progress){
            progressBar.value = progress
        }
    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.66;height:480;width:800}
}
##^##*/

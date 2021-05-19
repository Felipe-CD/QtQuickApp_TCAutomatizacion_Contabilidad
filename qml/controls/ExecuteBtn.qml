import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: openButton

    //Custom Properties
    property color colorDefault: "#4891d9"
    property color colorMouseOver: "#55AAFF"
    property color colorPressed: "#3F7EBD"
    property string textBtn: "Execute"

    QtObject{
        id: internal

        property var dynamicColor: if(openButton.down){
                                       openButton.down ? colorPressed : colorDefault
                                   }else{
                                       openButton.hovered ? colorMouseOver : colorDefault
                                   }
    }

    implicitWidth: 150
    implicitHeight: 40

    background: Rectangle{
        color: internal.dynamicColor
        radius: 10

        Label {
            id: labelBtn
            text: textBtn
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.bold: true
            font.pointSize: 16
            anchors.horizontalCenter: parent.horizontalCenter
            width: 30
            height: 30
            color: "#eceef0"
        }

        ColorOverlay{
            anchors.fill: labelBtn
            source: labelBtn
            color: "#ffffff"
            antialiasing: false
        }
    }
}

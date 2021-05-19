import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: openButton

    //Custom Properties
    property color colorDefault: "#4891d9"
    property color colorMouseOver: "#55AAFF"
    property color colorPressed: "#3F7EBD"
    property url btnSource: "../../images/svg_images/open_icon.svg"

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

        Image {
            id: iconBtn
            source: btnSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            width: 30
            height: 30
        }

        ColorOverlay{
            anchors.fill: iconBtn
            source: iconBtn
            color: "#ffffff"
            antialiasing: false
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:2;height:40;width:150}
}
##^##*/

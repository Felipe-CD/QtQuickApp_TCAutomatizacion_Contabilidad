import QtQuick 2.0
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Label{
    id: textLabel

    // Custom properties
    property color colorDefault: "#282c34"
    property color colorOnFocus: "#242831"
    property color colorMouseOver: "#282F38"
    height: 40
    verticalAlignment: Text.AlignVCenter

    QtObject{
        id: internal

        property var dynamicColor: if(textLabel.focus){
                                       textLabel.hovered ? colorOnFocus : colorDefault
                                   }else{
                                       textLabel.hovered ? colorMouseOver : colorDefault
                                   }
    }

    background: Rectangle{
        color: internal.dynamicColor
        radius: 10
    }
}

/*##^##
Designer {
    D{i:0;height:19;width:492}
}
##^##*/

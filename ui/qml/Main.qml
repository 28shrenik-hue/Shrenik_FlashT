import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    id: window
    width: 430
    height: 690
    visible: true
    title: "FlashTile"
    color: "#07101f"
    flags: Qt.Window | Qt.WindowStaysOnTopHint

    Component.onCompleted: {
        x = Screen.desktopAvailableWidth - width - 28
        y = 38
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0; color: "#0b1930" }
            GradientStop { position: 1; color: "#07101f" }
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 26
            spacing: 18

            RowLayout {
                Layout.fillWidth: true
                ColumnLayout {
                    spacing: 2
                    Text { text: "FLASHTILE"; color: "#eff7ff"; font.pixelSize: 22; font.bold: true; font.letterSpacing: 2 }
                    Text { text: "Knowledge that finds you."; color: "#7f96b8"; font.pixelSize: 12 }
                }
                Item { Layout.fillWidth: true }
                Rectangle {
                    width: 54; height: 54; radius: 17
                    gradient: Gradient {
                        GradientStop { position: 0; color: "#45d8ff" }
                        GradientStop { position: 1; color: "#7367ff" }
                    }
                    Text { anchors.centerIn: parent; text: "F"; color: "white"; font.pixelSize: 28; font.bold: true }
                }
            }

            ComboBox {
                id: topicPicker
                Layout.fillWidth: true
                model: learningService.topics
                currentIndex: model.indexOf(learningService.topic)
                onActivated: learningService.selectTopic(currentText)
            }

            Rectangle {
                id: card
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 28
                border.width: 1
                border.color: mouse.containsMouse ? "#55d8ff" : "#294366"
                gradient: Gradient {
                    GradientStop { position: 0; color: "#17345b" }
                    GradientStop { position: 0.55; color: "#102544" }
                    GradientStop { position: 1; color: "#121a39" }
                }
                scale: mouse.containsMouse ? 1.018 : 1
                Behavior on scale { NumberAnimation { duration: 180; easing.type: Easing.OutCubic } }

                MouseArea {
                    id: mouse
                    anchors.fill: parent
                    hoverEnabled: true
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 26
                    spacing: 14
                    Text { text: "TODAY'S FLASH"; color: "#5ce1ff"; font.pixelSize: 12; font.bold: true; font.letterSpacing: 1.5 }
                    Text { text: learningService.topic; color: "#f4a340"; font.pixelSize: 14; font.bold: true }
                    Text {
                        Layout.fillWidth: true
                        text: learningService.title
                        color: "white"
                        font.pixelSize: 31
                        font.bold: true
                        wrapMode: Text.WordWrap
                    }
                    Text {
                        Layout.fillWidth: true
                        text: learningService.description
                        color: "#b8cae2"
                        font.pixelSize: 16
                        lineHeight: 1.25
                        wrapMode: Text.WordWrap
                    }
                    Item { Layout.fillHeight: true }
                    RowLayout {
                        spacing: 10
                        Rectangle {
                            width: 90; height: 34; radius: 17; color: "#203a5e"
                            Text { anchors.centerIn: parent; text: "◷ " + learningService.minutes + " min"; color: "#d8e9ff" }
                        }
                        Rectangle {
                            width: 90; height: 34; radius: 17; color: "#203a5e"
                            Text { anchors.centerIn: parent; text: "+25 XP"; color: "#d8e9ff" }
                        }
                    }
                    Button {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 54
                        text: "Complete today's flash"
                        onClicked: learningService.completeLesson()
                    }
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Text { text: "⚡ " + learningService.xp + " XP"; color: "#cbdcf2"; font.pixelSize: 15; font.bold: true }
                Item { Layout.fillWidth: true }
                Text { text: "🔥 " + learningService.streak + " day streak"; color: "#cbdcf2"; font.pixelSize: 15; font.bold: true }
            }
            Label {
                id: message
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
                color: "#68edc6"
                text: ""
            }
        }
    }

    Connections {
        target: learningService
        function onCelebration(value) {
            message.text = value
            clearMessage.restart()
        }
    }
    Timer { id: clearMessage; interval: 3500; onTriggered: message.text = "" }
}


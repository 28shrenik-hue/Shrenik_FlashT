import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    id: window
    width: 430
    height: 730
    minimumWidth: 430
    maximumWidth: 430
    minimumHeight: 730
    maximumHeight: 730
    visible: true
    title: "FlashTile"
    color: "transparent"
    flags: Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

    property int selectedAnswer: -1
    property int flowStep: learningService.reviewMode ? 1 : 0
    property int pendingFlowStep: 0
    property string pendingFeedback: ""
    property string feedbackText: ""
    property color feedbackColor: "#9FB0CF"
    property int resetSeconds: 60
    property int breathElapsed: 0
    readonly property int breathPosition: breathElapsed % 12
    readonly property string breathPhase: breathPosition < 4 ? "Inhale" : (breathPosition < 6 ? "Hold" : "Exhale")
    readonly property int breathCount: breathPosition < 4 ? 4 - breathPosition : (breathPosition < 6 ? 6 - breathPosition : 12 - breathPosition)

    function moveToStep(step, message) {
        pendingFlowStep = step
        pendingFeedback = message
        stageTransition.restart()
    }

    Rectangle {
        anchors.fill: parent
        radius: 30
        border.color: "#263A66"
        border.width: 1
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#111A33" }
            GradientStop { position: 0.55; color: "#090F1E" }
            GradientStop { position: 1.0; color: "#050912" }
        }

        Item {
            anchors.fill: parent
            clip: true
            opacity: 0.20
            Repeater {
                model: 18
                Rectangle {
                    required property int index
                    width: index % 4 === 0 ? 3 : 2
                    height: width
                    radius: width / 2
                    color: index % 3 === 0 ? "#5CE1FF" : "#8175FF"
                    x: ((index * 83) % 410) + heroCard.tiltY * (0.35 + (index % 3) * 0.2)
                    y: ((index * 127) % 700) + heroCard.tiltX * (0.35 + (index % 4) * 0.15)
                    Behavior on x { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
                    Behavior on y { NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
                }
            }
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 22
            spacing: 13

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: 46

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton
                    onPressed: window.startSystemMove()
                }

                RowLayout {
                    anchors.fill: parent
                    spacing: 8
                    Rectangle {
                        Layout.preferredWidth: 40
                        Layout.preferredHeight: 40
                        radius: 12
                        clip: true
                        color: "#08112A"
                        border.width: 1
                        border.color: "#3C69B8"
                        Image {
                            anchors.fill: parent
                            source: "../../assets/branding/FlashTile_3D_Logo.png"
                            sourceClipRect: Qt.rect(185, 70, 880, 800)
                            fillMode: Image.PreserveAspectCrop
                            smooth: true
                            mipmap: true
                        }
                    }
                    Column {
                        spacing: 1
                        Text { text: "FLASHTILE"; color: "#EFF7FF"; font.pixelSize: 19; font.bold: true; font.letterSpacing: 2 }
                        Text { text: "Knowledge that finds you."; color: "#7F96B8"; font.pixelSize: 11 }
                    }
                    Item { Layout.fillWidth: true }
                    Text { text: "⚡ " + learningService.xp; color: "#83E8FF"; font.bold: true }
                    Text { text: "🔥 " + learningService.streak; color: "#FFCB68"; font.bold: true }
                    Button {
                        text: "×"
                        flat: true
                        Layout.preferredWidth: 34
                        onClicked: Qt.quit()
                        contentItem: Text {
                            text: parent.text; color: "#AAB8D5"; font.pixelSize: 22
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                }
            }

            ComboBox {
                Layout.fillWidth: true
                model: learningService.topics
                currentIndex: model.indexOf(learningService.topic)
                onActivated: {
                    selectedAnswer = -1
                    flowStep = 0
                    feedbackText = ""
                    learningService.selectTopic(currentText)
                }
            }

            Rectangle {
                id: heroCard
                Layout.fillWidth: true
                Layout.preferredHeight: 414
                radius: 28
                border.width: 1
                border.color: hover.hovered ? "#58DFFF" : "#3C5E9D"
                color: "#101C39"
                transformOrigin: Item.Center
                property real tiltX: 0
                property real tiltY: 0
                property real transitionOffset: 0
                property real transitionScale: 1
                property real transitionTilt: 0
                property real transitionOpacity: 1
                property real sheenX: -90
                property real sheenOpacity: 0
                clip: true
                scale: hover.hovered ? 1.018 : 1.0
                opacity: transitionOpacity

                Behavior on scale { NumberAnimation { duration: 170; easing.type: Easing.OutCubic } }
                Behavior on tiltX { SpringAnimation { spring: 3; damping: 0.35 } }
                Behavior on tiltY { SpringAnimation { spring: 3; damping: 0.35 } }
                Behavior on border.color { ColorAnimation { duration: 180 } }

                transform: [
                    Translate {
                        x: heroCard.transitionOffset
                    },
                    Rotation {
                        origin.x: heroCard.width / 2; origin.y: heroCard.height / 2
                        axis { x: 1; y: 0; z: 0 }
                        angle: heroCard.tiltX
                    },
                    Rotation {
                        origin.x: heroCard.width / 2; origin.y: heroCard.height / 2
                        axis { x: 0; y: 1; z: 0 }
                        angle: heroCard.tiltY + heroCard.transitionTilt
                    },
                    Scale {
                        origin.x: heroCard.width / 2
                        origin.y: heroCard.height / 2
                        xScale: heroCard.transitionScale
                        yScale: heroCard.transitionScale
                    }
                ]

                Rectangle {
                    anchors.fill: parent
                    anchors.margins: 1
                    radius: 27
                    opacity: 0.91
                    gradient: Gradient {
                        GradientStop { position: 0; color: "#17396A" }
                        GradientStop { position: 0.46; color: "#141F42" }
                        GradientStop { position: 1; color: "#24133D" }
                    }
                }

                Rectangle {
                    width: 190; height: 190; radius: 95
                    x: Math.max(-50, Math.min(heroCard.width - width + 50, hover.point.position.x - width / 2))
                    y: Math.max(-50, Math.min(heroCard.height - height + 50, hover.point.position.y - height / 2))
                    color: "#FF9900"
                    opacity: hover.hovered ? 0.12 : 0
                    Behavior on opacity { NumberAnimation { duration: 200 } }
                }

                Rectangle {
                    width: 54
                    height: heroCard.height * 1.35
                    x: heroCard.sheenX
                    y: -heroCard.height * 0.18
                    rotation: 16
                    color: "#BCEEFF"
                    opacity: heroCard.sheenOpacity
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 24
                    spacing: 11

                    RowLayout {
                        Layout.fillWidth: true
                        Rectangle {
                            width: 62; height: 62; radius: 19
                            color: "#213151"; border.color: "#FFB14A"
                            Text { anchors.centerIn: parent; text: "F"; color: "#FFB14A"; font.pixelSize: 30; font.bold: true }
                            SequentialAnimation on scale {
                                loops: Animation.Infinite
                                NumberAnimation { to: 1.05; duration: 1300; easing.type: Easing.InOutSine }
                                NumberAnimation { to: 1.0; duration: 1300; easing.type: Easing.InOutSine }
                            }
                        }
                        Column {
                            Layout.fillWidth: true
                            Text {
                                text: learningService.reviewMode ? "REVIEW FLASH" : "TODAY'S FLASH"
                                color: learningService.reviewMode ? "#68EDC6" : "#5CE1FF"
                                font.pixelSize: 11
                                font.bold: true
                                font.letterSpacing: 1.5
                            }
                            Text {
                                width: parent.width
                                text: learningService.topic
                                color: "#FFB14A"
                                font.pixelSize: 14
                                font.bold: true
                                elide: Text.ElideRight
                            }
                        }
                        Rectangle {
                            width: 74; height: 30; radius: 15; color: "#203A5E"
                            Text { anchors.centerIn: parent; text: "◷ " + learningService.minutes + " min"; color: "#D8E9FF"; font.pixelSize: 12 }
                        }
                    }

                    Text {
                        Layout.fillWidth: true; text: learningService.title
                        color: "white"; font.pixelSize: 27; font.bold: true; wrapMode: Text.WordWrap
                    }
                    StackLayout {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        Layout.minimumHeight: 0
                        currentIndex: flowStep

                        ColumnLayout {
                            spacing: 11
                            Text {
                                text: "CORE CONCEPT"
                                color: "#5CE1FF"
                                font.pixelSize: 11
                                font.bold: true
                                font.letterSpacing: 1.3
                            }
                            Text {
                                Layout.fillWidth: true
                                text: learningService.description
                                color: "#C9D6F2"
                                font.pixelSize: 14
                                lineHeight: 1.18
                                wrapMode: Text.WordWrap
                            }
                            Rectangle {
                                Layout.fillWidth: true
                                Layout.preferredHeight: whyText.implicitHeight + 18
                                radius: 11
                                color: "#172A49"
                                border.color: "#355072"
                                Text {
                                    id: whyText
                                    anchors.fill: parent
                                    anchors.margins: 9
                                    text: "Why it matters: " + learningService.whyItMatters
                                    color: "#BCE0F6"
                                    font.pixelSize: 12
                                    wrapMode: Text.WordWrap
                                }
                            }
                            Item { Layout.fillHeight: true }
                            Button {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 44
                                text: "Practical scenario  →"
                                onClicked: moveToStep(1, "Apply the idea to a realistic situation.")
                                background: Rectangle {
                                    radius: 13
                                    gradient: Gradient {
                                        GradientStop { position: 0; color: "#FF9900" }
                                        GradientStop { position: 1; color: "#7B4DFF" }
                                    }
                                }
                                contentItem: Text {
                                    text: parent.text; color: "white"; font.bold: true; font.pixelSize: 13
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                            }
                        }

                        ColumnLayout {
                            spacing: 11
                            Text {
                                text: learningService.reviewMode ? "QUICK RECALL SCENARIO" : "PRACTICAL SCENARIO"
                                color: learningService.reviewMode ? "#68EDC6" : "#FFB14A"
                                font.pixelSize: 11
                                font.bold: true
                                font.letterSpacing: 1.3
                            }
                            Text {
                                Layout.fillWidth: true
                                text: learningService.scenario
                                color: "#EFF5FF"
                                font.pixelSize: 14
                                lineHeight: 1.2
                                wrapMode: Text.WordWrap
                            }
                            Item { Layout.fillHeight: true }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 9
                                Button {
                                    visible: !learningService.reviewMode
                                    Layout.preferredWidth: visible ? 82 : 0
                                    Layout.preferredHeight: 42
                                    text: "Back"
                                    onClicked: moveToStep(0, "Understand the core concept before applying it.")
                                }
                                Button {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 42
                                    text: learningService.reviewMode ? "Answer recall  →" : "Go deeper  →"
                                    onClicked: moveToStep(
                                        learningService.reviewMode ? 3 : 2,
                                        learningService.reviewMode
                                            ? "Retrieve the idea without reopening the lesson."
                                            : "Explore the detail behind the scenario."
                                    )
                                }
                            }
                        }

                        ColumnLayout {
                            spacing: 11
                            Text {
                                text: "GO DEEPER"
                                color: "#8175FF"
                                font.pixelSize: 11
                                font.bold: true
                                font.letterSpacing: 1.3
                            }
                            Text {
                                Layout.fillWidth: true
                                text: learningService.deeper
                                color: "#E0E9F8"
                                font.pixelSize: 14
                                lineHeight: 1.32
                                wrapMode: Text.WordWrap
                            }
                            Item { Layout.fillHeight: true }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 9
                                Button {
                                    Layout.preferredWidth: 82
                                    Layout.preferredHeight: 42
                                    text: "Back"
                                    onClicked: moveToStep(1, "Return to the practical scenario.")
                                }
                                Button {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 42
                                    text: "Knowledge check  →"
                                    onClicked: moveToStep(3, "Use a new question to test understanding.")
                                }
                            }
                        }

                        ColumnLayout {
                            spacing: 9
                            Text {
                                text: learningService.reviewMode ? "RECALL CHECK" : "KNOWLEDGE CHECK"
                                color: "#68EDC6"
                                font.pixelSize: 11
                                font.bold: true
                                font.letterSpacing: 1.3
                            }
                            Text {
                                Layout.fillWidth: true
                                text: learningService.question
                                color: "#EFF5FF"
                                font.pixelSize: 13
                                font.bold: true
                                wrapMode: Text.WordWrap
                            }
                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 6
                                Repeater {
                                    model: learningService.options
                                    Button {
                                        required property int index
                                        required property string modelData
                                        Layout.fillWidth: true
                                        Layout.preferredHeight: 34
                                        text: modelData
                                        checkable: true
                                        checked: window.selectedAnswer === index
                                        onClicked: window.selectedAnswer = index
                                        background: Rectangle {
                                            radius: 10
                                            color: parent.checked ? "#285C8D" : "#172A49"
                                            border.color: parent.checked ? "#62DFFF" : "#355072"
                                        }
                                        contentItem: Text {
                                            text: parent.text
                                            color: "#EAF3FF"
                                            font.pixelSize: 11
                                            font.bold: parent.checked
                                            horizontalAlignment: Text.AlignHCenter
                                            verticalAlignment: Text.AlignVCenter
                                        }
                                    }
                                }
                            }
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 7
                                Button {
                                    Layout.preferredWidth: 68
                                    Layout.preferredHeight: 38
                                    text: "Back"
                                    onClicked: moveToStep(
                                        learningService.reviewMode ? 1 : 2,
                                        learningService.reviewMode
                                            ? "Return to the recall scenario."
                                            : "Review the deeper explanation."
                                    )
                                }
                                Button {
                                    Layout.preferredWidth: 76
                                    Layout.preferredHeight: 38
                                    text: "Check"
                                    enabled: selectedAnswer >= 0
                                    onClicked: learningService.checkAnswer(selectedAnswer)
                                }
                                Button {
                                    Layout.fillWidth: true
                                    Layout.preferredHeight: 38
                                    text: learningService.quizPassed
                                        ? (learningService.reviewMode ? "Complete • +10 XP" : "Complete • +25 XP")
                                        : "Complete"
                                    enabled: learningService.quizPassed
                                    onClicked: {
                                        const wasReview = learningService.reviewMode
                                        if (learningService.completeLesson()) {
                                            flowStep = wasReview ? 5 : 4
                                            celebrate.restart()
                                        }
                                    }
                                    background: Rectangle {
                                        radius: 13
                                        opacity: parent.enabled ? 1 : 0.45
                                        gradient: Gradient {
                                            GradientStop { position: 0; color: "#FF9900" }
                                            GradientStop { position: 1; color: "#7B4DFF" }
                                        }
                                    }
                                    contentItem: Text {
                                        text: parent.text; color: "white"; font.bold: true; font.pixelSize: 13
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }
                            }
                        }

                        ColumnLayout {
                            spacing: 12
                            Item { Layout.fillHeight: true }
                            Text {
                                Layout.fillWidth: true
                                text: "✓"
                                color: "#68EDC6"
                                font.pixelSize: 42
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Text {
                                Layout.fillWidth: true
                                text: "How confident do you feel?"
                                color: "white"
                                font.pixelSize: 19
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Text {
                                Layout.fillWidth: true
                                text: "Your answer sets the next review—not your score."
                                color: "#B7C7E1"
                                font.pixelSize: 12
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Button {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 40
                                text: "Got it"
                                onClicked: {
                                    learningService.setConfidence("got_it")
                                    flowStep = 5
                                }
                            }
                            Button {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 40
                                text: "Need practice"
                                onClicked: {
                                    learningService.setConfidence("need_practice")
                                    flowStep = 5
                                }
                            }
                            Button {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 40
                                text: "Review later"
                                onClicked: {
                                    learningService.setConfidence("review_later")
                                    flowStep = 5
                                }
                            }
                            Item { Layout.fillHeight: true }
                        }

                        ColumnLayout {
                            spacing: 14
                            Item { Layout.fillHeight: true }
                            Text {
                                Layout.fillWidth: true
                                text: "✓"
                                color: "#68EDC6"
                                font.pixelSize: 58
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Text {
                                Layout.fillWidth: true
                                text: learningService.reviewMode ? "Recall complete" : "Today's flash is complete"
                                color: "white"
                                font.pixelSize: 20
                                font.bold: true
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Text {
                                Layout.fillWidth: true
                                text: learningService.reviewMode
                                    ? "Mastery: " + learningService.masteryLabel + " • " + learningService.nextReviewText
                                    : learningService.masteryLabel + " • " + learningService.nextReviewText
                                color: "#C9D6F2"
                                font.pixelSize: 13
                                horizontalAlignment: Text.AlignHCenter
                            }
                            Item { Layout.fillHeight: true }
                            Button {
                                Layout.fillWidth: true
                                Layout.preferredHeight: 46
                                text: "Next flash  →"
                                onClicked: nextFlashTransition.restart()
                            }
                        }
                    }
                }

                HoverHandler {
                    id: hover
                    onPointChanged: {
                        const nx = (point.position.x / heroCard.width - 0.5) * 2
                        const ny = (point.position.y / heroCard.height - 0.5) * 2
                        heroCard.tiltY = nx * 7
                        heroCard.tiltX = -ny * 7
                    }
                    onHoveredChanged: {
                        if (!hovered) {
                            heroCard.tiltX = 0
                            heroCard.tiltY = 0
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 62
                radius: 15
                color: "#0E1729"
                border.color: feedbackText === "" ? "#202F4E" : feedbackColor
                Text {
                    anchors.centerIn: parent
                    width: parent.width - 24
                    text: feedbackText === "" ?
                        (flowStep === 0 ? "Start with the core concept." :
                        flowStep === 1 ? "Apply the idea to a practical scenario." :
                        flowStep === 2 ? "Go deeper when you are ready." :
                        flowStep === 3 ? "Choose the best answer, then select Check." :
                        flowStep === 4 ? "Choose when this concept should return." :
                        "Continue whenever you want another flash.") : feedbackText
                    color: feedbackText === "" ? "#9FB0CF" : feedbackColor
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                }
            }

            Item { Layout.fillHeight: true }
            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: 42

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Button {
                        id: bookmarkButton
                        anchors.centerIn: parent
                        width: 48
                        height: 42
                        Accessible.name: "Open saved lesson bookmarks"
                        flat: true
                        onClicked: bookmarksPopup.open()
                        ToolTip.visible: hovered
                        ToolTip.text: learningService.bookmarkCount === 0
                            ? "Bookmark and review lessons"
                            : "Saved review • " + learningService.bookmarkCount
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: bookmarkButton.hovered ? 1.08 : 1
                                color: bookmarkButton.hovered ? "#2D294D" : "#101D34"
                                border.width: 1
                                border.color: learningService.bookmarked ? "#FFCB68" : "#4E5E7B"
                                Behavior on scale { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
                                Behavior on color { ColorAnimation { duration: 160 } }
                                Behavior on border.color { ColorAnimation { duration: 160 } }
                                Text {
                                    anchors.centerIn: parent
                                    text: learningService.bookmarked ? "★" : "☆"
                                    color: learningService.bookmarked ? "#FFCB68" : "#AFC1DD"
                                    font.pixelSize: 22
                                }
                                Rectangle {
                                    visible: learningService.bookmarkCount > 0
                                    width: 15
                                    height: 15
                                    radius: 7.5
                                    anchors.right: parent.right
                                    anchors.top: parent.top
                                    color: "#FFCB68"
                                    Text {
                                        anchors.centerIn: parent
                                        text: learningService.bookmarkCount
                                        color: "#11172F"
                                        font.pixelSize: 9
                                        font.bold: true
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Button {
                        id: resetButton
                        anchors.centerIn: parent
                        width: 48
                        height: 42
                        Accessible.name: "Open 60-second guided breathing reset"
                        flat: true
                        onClicked: resetPopup.open()
                        ToolTip.visible: hovered
                        ToolTip.text: "Guided 60-second reset"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: resetButton.hovered ? 1.08 : 1
                                color: resetButton.hovered ? "#17345B" : "#101D34"
                                border.width: 1
                                border.color: resetButton.hovered ? "#68EDC6" : "#3D6F92"
                                Behavior on scale { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
                                Behavior on color { ColorAnimation { duration: 160 } }
                                Behavior on border.color { ColorAnimation { duration: 160 } }

                                Text {
                                    anchors.centerIn: parent
                                    anchors.verticalCenterOffset: -1
                                    text: "≋"
                                    color: resetButton.hovered ? "#68EDC6" : "#83E8FF"
                                    font.pixelSize: 23
                                    font.bold: true
                                    Behavior on color { ColorAnimation { duration: 160 } }
                                }
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Button {
                        id: notesButton
                        anchors.centerIn: parent
                        width: 48
                        height: 42
                        Accessible.name: "Open quick learning notes"
                        flat: true
                        onClicked: notesPopup.open()
                        ToolTip.visible: hovered
                        ToolTip.text: learningService.lessonNote === "" ? "Add quick note" : "Edit quick note"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: notesButton.hovered ? 1.08 : 1
                                color: notesButton.hovered ? "#20314A" : "#101D34"
                                border.width: 1
                                border.color: learningService.lessonNote === "" ? "#4E5E7B" : "#8175FF"
                                Behavior on scale { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
                                Behavior on color { ColorAnimation { duration: 160 } }
                                Behavior on border.color { ColorAnimation { duration: 160 } }

                                Text {
                                    anchors.centerIn: parent
                                    anchors.verticalCenterOffset: -1
                                    text: "✎"
                                    color: learningService.lessonNote === "" ? "#AFC1DD" : "#B8AFFF"
                                    font.pixelSize: 22
                                    font.bold: true
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    Popup {
        id: bookmarksPopup
        objectName: "bookmarksPopup"
        anchors.centerIn: Overlay.overlay
        width: 350
        height: 420
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 22

        background: Rectangle {
            radius: 26
            border.width: 1
            border.color: "#9A7436"
            gradient: Gradient {
                GradientStop { position: 0; color: "#29213A" }
                GradientStop { position: 1; color: "#11172F" }
            }
        }

        contentItem: ColumnLayout {
            spacing: 10
            Text {
                Layout.fillWidth: true
                text: "SAVED REVIEW"
                color: "#FFCB68"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 1.5
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                Layout.fillWidth: true
                text: "Return to important concepts without leaving the tile."
                color: "#B7C7E1"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            Button {
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                text: learningService.bookmarked ? "Remove current bookmark" : "Bookmark current lesson"
                onClicked: learningService.toggleBookmark()
            }
            Text {
                visible: learningService.bookmarkCount === 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                text: "No saved lessons yet.\nBookmark the current lesson to begin."
                color: "#8192AE"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            ListView {
                id: bookmarkList
                visible: learningService.bookmarkCount > 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 7
                model: learningService.bookmarkItems
                delegate: Rectangle {
                    required property int index
                    required property string modelData
                    width: bookmarkList.width
                    height: 54
                    radius: 12
                    color: "#101D34"
                    border.color: "#4A526F"
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 7
                        Button {
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            flat: true
                            text: modelData
                            onClicked: {
                                learningService.openBookmark(index)
                                bookmarksPopup.close()
                                flowStep = 0
                                selectedAnswer = -1
                                feedbackText = "Saved lesson opened."
                                feedbackColor = "#FFCB68"
                            }
                            contentItem: Text {
                                text: parent.text
                                color: "#EAF3FF"
                                font.pixelSize: 11
                                elide: Text.ElideRight
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                        Button {
                            Layout.preferredWidth: 34
                            Layout.fillHeight: true
                            flat: true
                            text: "×"
                            onClicked: learningService.removeBookmark(index)
                            contentItem: Text {
                                text: parent.text
                                color: "#AFC1DD"
                                font.pixelSize: 18
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }
            }
            Button {
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                text: "Close"
                onClicked: bookmarksPopup.close()
            }
        }
    }

    Popup {
        id: notesPopup
        objectName: "notesPopup"
        anchors.centerIn: Overlay.overlay
        width: 340
        height: 350
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 24

        onOpened: {
            noteEditor.text = learningService.lessonNote
            noteEditor.forceActiveFocus()
        }

        background: Rectangle {
            radius: 26
            border.width: 1
            border.color: "#6656B8"
            gradient: Gradient {
                GradientStop { position: 0; color: "#22234A" }
                GradientStop { position: 1; color: "#11172F" }
            }
        }

        contentItem: ColumnLayout {
            spacing: 11
            Text {
                Layout.fillWidth: true
                text: "QUICK NOTES"
                color: "#B8AFFF"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 1.5
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                Layout.fillWidth: true
                text: learningService.title
                color: "white"
                font.pixelSize: 18
                font.bold: true
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            TextArea {
                id: noteEditor
                Layout.fillWidth: true
                Layout.preferredHeight: 145
                placeholderText: "Capture one useful takeaway…"
                wrapMode: TextEdit.Wrap
                font.pixelSize: 13
                color: "#EAF3FF"
                placeholderTextColor: "#71839F"
                onTextChanged: {
                    if (length > 500)
                        text = text.slice(0, 500)
                }
                background: Rectangle {
                    radius: 13
                    color: "#0D1830"
                    border.color: noteEditor.activeFocus ? "#8175FF" : "#344866"
                }
            }
            Text {
                Layout.fillWidth: true
                text: noteEditor.length + " / 500"
                color: "#8397B5"
                font.pixelSize: 11
                horizontalAlignment: Text.AlignRight
            }
            Item { Layout.fillHeight: true }
            RowLayout {
                Layout.fillWidth: true
                spacing: 9
                Button {
                    Layout.preferredWidth: 90
                    Layout.preferredHeight: 42
                    text: "Cancel"
                    onClicked: notesPopup.close()
                }
                Button {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 42
                    text: noteEditor.text.trim() === "" && learningService.lessonNote !== ""
                        ? "Clear note" : "Save note"
                    enabled: noteEditor.text.trim() !== "" || learningService.lessonNote !== ""
                    onClicked: {
                        learningService.saveLessonNote(noteEditor.text)
                        notesPopup.close()
                    }
                    background: Rectangle {
                        radius: 13
                        gradient: Gradient {
                            GradientStop { position: 0; color: "#5B55D6" }
                            GradientStop { position: 1; color: "#7B4DFF" }
                        }
                    }
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }
    }

    Popup {
        id: resetPopup
        anchors.centerIn: Overlay.overlay
        width: 330
        height: 390
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 24

        onOpened: {
            resetSeconds = 60
            breathElapsed = 0
            resetTimer.start()
        }
        onClosed: resetTimer.stop()

        background: Rectangle {
            radius: 26
            border.width: 1
            border.color: "#4F75A8"
            gradient: Gradient {
                GradientStop { position: 0; color: "#17345B" }
                GradientStop { position: 1; color: "#11172F" }
            }
        }

        contentItem: ColumnLayout {
            spacing: 12
            Text {
                Layout.fillWidth: true
                text: "60-SECOND RESET"
                color: "#5CE1FF"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 1.5
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                Layout.fillWidth: true
                text: resetSeconds > 0 ? resetSeconds + " seconds" : "Complete"
                color: "white"
                font.pixelSize: 25
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
            }
            Item {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 150
                Layout.preferredHeight: 150
                Rectangle {
                    anchors.centerIn: parent
                    width: 112
                    height: 112
                    radius: 56
                    color: "#285C8D"
                    border.width: 2
                    border.color: "#68EDC6"
                    SequentialAnimation on scale {
                        running: resetTimer.running
                        loops: Animation.Infinite
                        NumberAnimation { from: 0.82; to: 1.18; duration: 4000; easing.type: Easing.InOutSine }
                        PauseAnimation { duration: 2000 }
                        NumberAnimation { from: 1.18; to: 0.82; duration: 6000; easing.type: Easing.InOutSine }
                    }
                    Text {
                        anchors.centerIn: parent
                        text: resetSeconds > 0 ? breathPhase + "\n" + breathCount : "✓"
                        color: "white"
                        font.pixelSize: 18
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }
            Text {
                Layout.fillWidth: true
                text: resetSeconds > 0 ? "Follow the circle gently. No data is recorded." : "Reset complete. Return when you are ready."
                color: "#B8CAE2"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            Item { Layout.fillHeight: true }
            Button {
                Layout.fillWidth: true
                Layout.preferredHeight: 42
                text: resetSeconds > 0 ? "End reset" : "Return to learning"
                onClicked: resetPopup.close()
            }
        }
    }

    Timer {
        id: resetTimer
        interval: 1000
        repeat: true
        onTriggered: {
            if (resetSeconds <= 1) {
                resetSeconds = 0
                stop()
            } else {
                resetSeconds -= 1
                breathElapsed += 1
            }
        }
    }

    Connections {
        target: learningService
        function onQuizResult(value, correct) {
            feedbackText = value
            feedbackColor = correct ? "#68EDC6" : "#FFB45E"
        }
        function onCelebration(value) {
            feedbackText = value
            feedbackColor = value.indexOf("+") === 0 ? "#68EDC6" : "#9FB0CF"
        }
    }

    SequentialAnimation {
        id: stageTransition
        running: false

        ParallelAnimation {
            NumberAnimation {
                target: heroCard; property: "transitionOffset"
                from: 0; to: -32; duration: 140; easing.type: Easing.InCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionScale"
                from: 1; to: 0.985; duration: 140; easing.type: Easing.InCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionTilt"
                from: 0; to: -2.5; duration: 140; easing.type: Easing.InOutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionOpacity"
                from: 1; to: 0.10; duration: 130; easing.type: Easing.InCubic
            }
        }

        ScriptAction {
            script: {
                flowStep = pendingFlowStep
                feedbackText = pendingFeedback
                feedbackColor = "#9FB0CF"
                heroCard.transitionOffset = 32
                heroCard.transitionScale = 0.985
                heroCard.transitionTilt = 2.5
                heroCard.transitionOpacity = 0.10
            }
        }

        ParallelAnimation {
            NumberAnimation {
                target: heroCard; property: "transitionOffset"
                from: 32; to: 0; duration: 220; easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionScale"
                from: 0.985; to: 1; duration: 220; easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionTilt"
                from: 2.5; to: 0; duration: 220; easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionOpacity"
                from: 0.10; to: 1; duration: 200; easing.type: Easing.OutCubic
            }
        }
    }

    SequentialAnimation {
        id: nextFlashTransition
        running: false

        ParallelAnimation {
            NumberAnimation {
                target: heroCard; property: "transitionOffset"
                from: 0; to: -78; duration: 240; easing.type: Easing.InCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionScale"
                from: 1; to: 0.94; duration: 240; easing.type: Easing.InCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionTilt"
                from: 0; to: -7; duration: 240; easing.type: Easing.InOutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionOpacity"
                from: 1; to: 0.08; duration: 220; easing.type: Easing.InCubic
            }
        }

        ScriptAction {
            script: {
                learningService.nextLesson()
                flowStep = 0
                selectedAnswer = -1
                feedbackText = ""
                heroCard.transitionOffset = 78
                heroCard.transitionScale = 0.94
                heroCard.transitionTilt = 7
                heroCard.transitionOpacity = 0.08
                heroCard.sheenX = -90
                heroCard.sheenOpacity = 0
            }
        }

        ParallelAnimation {
            NumberAnimation {
                target: heroCard; property: "transitionOffset"
                from: 78; to: 0; duration: 360; easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionScale"
                from: 0.94; to: 1; duration: 360; easing.type: Easing.OutBack
            }
            NumberAnimation {
                target: heroCard; property: "transitionTilt"
                from: 7; to: 0; duration: 360; easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: heroCard; property: "transitionOpacity"
                from: 0.08; to: 1; duration: 280; easing.type: Easing.OutCubic
            }
            NumberAnimation {
                target: heroCard; property: "sheenX"
                from: -90; to: heroCard.width + 90; duration: 520; easing.type: Easing.OutCubic
            }
            SequentialAnimation {
                NumberAnimation {
                    target: heroCard; property: "sheenOpacity"
                    from: 0; to: 0.13; duration: 150
                }
                NumberAnimation {
                    target: heroCard; property: "sheenOpacity"
                    from: 0.13; to: 0; duration: 300
                }
            }
        }
    }

    ParallelAnimation {
        id: celebrate
        NumberAnimation { target: heroCard; property: "scale"; from: 1.0; to: 1.06; duration: 180; easing.type: Easing.OutBack }
        SequentialAnimation {
            NumberAnimation { target: heroCard; property: "opacity"; to: 0.82; duration: 90 }
            NumberAnimation { target: heroCard; property: "opacity"; to: 1.0; duration: 180 }
        }
    }
}

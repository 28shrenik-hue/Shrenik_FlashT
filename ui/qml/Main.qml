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
        if (learningService.reducedMotion) {
            flowStep = step
            feedbackText = message
            feedbackColor = "#9FB0CF"
            return
        }
        pendingFlowStep = step
        pendingFeedback = message
        stageTransition.restart()
    }

    function advanceLesson() {
        learningService.nextLesson()
        flowStep = 0
        selectedAnswer = -1
        feedbackText = ""
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
                    x: ((index * 83) % 410) + (learningService.reducedMotion ? 0 : heroCard.tiltY * (0.35 + (index % 3) * 0.2))
                    y: ((index * 127) % 700) + (learningService.reducedMotion ? 0 : heroCard.tiltX * (0.35 + (index % 4) * 0.15))
                    Behavior on x { enabled: !learningService.reducedMotion; NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
                    Behavior on y { enabled: !learningService.reducedMotion; NumberAnimation { duration: 220; easing.type: Easing.OutCubic } }
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
                        id: teamButton
                        text: "👥"
                        flat: true
                        Layout.preferredWidth: 30
                        Accessible.name: "Open Team Board demo"
                        onClicked: teamBoardPopup.open()
                        ToolTip.visible: hovered
                        ToolTip.text: "Team Board • Demo"
                        ToolTip.delay: 450
                        contentItem: Text {
                            text: parent.text
                            color: "#A8E5DA"
                            font.pixelSize: 15
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                    Button {
                        text: "×"
                        flat: true
                        Layout.preferredWidth: 34
                        Accessible.name: "Close FlashTile"
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
                Accessible.name: "Learning topic"
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
                scale: hover.hovered && !learningService.reducedMotion ? 1.018 : 1.0
                opacity: transitionOpacity

                Behavior on scale { enabled: !learningService.reducedMotion; NumberAnimation { duration: 170; easing.type: Easing.OutCubic } }
                Behavior on tiltX { enabled: !learningService.reducedMotion; SpringAnimation { spring: 3; damping: 0.35 } }
                Behavior on tiltY { enabled: !learningService.reducedMotion; SpringAnimation { spring: 3; damping: 0.35 } }
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
                    Behavior on opacity { enabled: !learningService.reducedMotion; NumberAnimation { duration: 200 } }
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
                                running: !learningService.reducedMotion
                                loops: Animation.Infinite
                                NumberAnimation { to: 1.05; duration: 1300; easing.type: Easing.InOutSine }
                                NumberAnimation { to: 1.0; duration: 1300; easing.type: Easing.InOutSine }
                            }
                        }
                        Column {
                            Layout.fillWidth: true
                            Text {
                                text: learningService.reviewMode
                                    ? "REVIEW FLASH"
                                    : (learningService.goalActive
                                        ? "GUIDED • " + learningService.goalProgressText.toUpperCase()
                                        : "TODAY'S FLASH")
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
                                            if (!learningService.reducedMotion)
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
                                onClicked: learningService.reducedMotion
                                    ? advanceLesson()
                                    : nextFlashTransition.restart()
                            }
                        }
                    }
                }

                HoverHandler {
                    id: hover
                    onPointChanged: {
                        if (learningService.reducedMotion)
                            return
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
                        id: goalButton
                        anchors.centerIn: parent
                        width: 48
                        height: 42
                        Accessible.name: "Choose a guided learning goal"
                        flat: true
                        onClicked: goalPopup.open()
                        ToolTip.visible: hovered
                        ToolTip.text: "Learning Goals"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: goalButton.hovered && !learningService.reducedMotion ? 1.08 : 1
                                color: goalButton.hovered ? "#17345B" : "#101D34"
                                border.width: 1
                                border.color: learningService.goalActive ? "#68EDC6" : "#4E5E7B"
                                Behavior on scale { enabled: !learningService.reducedMotion; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
                                Text {
                                    anchors.centerIn: parent
                                    text: "◎"
                                    color: learningService.goalActive ? "#68EDC6" : "#AFC1DD"
                                    font.pixelSize: 22
                                    font.bold: true
                                }
                            }
                        }
                    }
                }

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
                        ToolTip.text: "Saved Lessons"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: bookmarkButton.hovered && !learningService.reducedMotion ? 1.08 : 1
                                color: bookmarkButton.hovered ? "#2D294D" : "#101D34"
                                border.width: 1
                                border.color: learningService.bookmarked ? "#FFCB68" : "#4E5E7B"
                                Behavior on scale { enabled: !learningService.reducedMotion; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
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
                        ToolTip.text: "Meditation"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: resetButton.hovered && !learningService.reducedMotion ? 1.08 : 1
                                color: resetButton.hovered ? "#17345B" : "#101D34"
                                border.width: 1
                                border.color: resetButton.hovered ? "#68EDC6" : "#3D6F92"
                                Behavior on scale { enabled: !learningService.reducedMotion; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
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
                        id: discoveryButton
                        anchors.centerIn: parent
                        width: 48
                        height: 42
                        Accessible.name: "Open Daily Discovery"
                        flat: true
                        onClicked: discoveryPopup.open()
                        ToolTip.visible: hovered
                        ToolTip.text: "Daily Discovery"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: discoveryButton.hovered && !learningService.reducedMotion ? 1.08 : 1
                                color: discoveryButton.hovered ? "#3A2B18" : "#101D34"
                                border.width: 1
                                border.color: discoveryButton.hovered ? "#FFCB68" : "#6F6042"
                                Behavior on scale { enabled: !learningService.reducedMotion; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
                                Text {
                                    anchors.centerIn: parent
                                    text: "✦"
                                    color: discoveryButton.hovered ? "#FFCB68" : "#D8C28A"
                                    font.pixelSize: 20
                                    font.bold: true
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
                        ToolTip.text: "Quick Notes"
                        ToolTip.delay: 450

                        contentItem: Item {
                            Rectangle {
                                anchors.centerIn: parent
                                width: 38
                                height: 38
                                radius: 19
                                scale: notesButton.hovered && !learningService.reducedMotion ? 1.08 : 1
                                color: notesButton.hovered ? "#20314A" : "#101D34"
                                border.width: 1
                                border.color: learningService.lessonNote === "" ? "#4E5E7B" : "#8175FF"
                                Behavior on scale { enabled: !learningService.reducedMotion; NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }
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
        id: teamBoardPopup
        objectName: "teamBoardPopup"
        anchors.centerIn: Overlay.overlay
        width: 370
        height: 625
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 22

        background: Rectangle {
            radius: 26
            border.width: 1
            border.color: "#4F8D86"
            gradient: Gradient {
                GradientStop { position: 0; color: "#173A40" }
                GradientStop { position: 0.42; color: "#17243A" }
                GradientStop { position: 1; color: "#11172F" }
            }
        }

        contentItem: ColumnLayout {
            spacing: 10
            RowLayout {
                Layout.fillWidth: true
                Text {
                    text: "TEAM BOARD"
                    color: "#68EDC6"
                    font.pixelSize: 12
                    font.bold: true
                    font.letterSpacing: 1.5
                }
                Item { Layout.fillWidth: true }
                Rectangle {
                    Layout.preferredWidth: 82
                    Layout.preferredHeight: 24
                    radius: 12
                    color: "#3B2F16"
                    border.color: "#A88743"
                    Text {
                        anchors.centerIn: parent
                        text: "DEMO MODE"
                        color: "#FFCB68"
                        font.pixelSize: 9
                        font.bold: true
                        font.letterSpacing: 0.8
                    }
                }
            }
            Text {
                Layout.fillWidth: true
                text: learningService.teamName
                color: "white"
                font.pixelSize: 23
                font.bold: true
            }
            Text {
                Layout.fillWidth: true
                text: "A preview of shared learning progress and recognition."
                color: "#AFC1DD"
                font.pixelSize: 11
                wrapMode: Text.WordWrap
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 7
                Repeater {
                    model: [
                        ["TEAM XP", learningService.teamXp],
                        ["STREAK", learningService.teamStreak + " days"],
                        ["LESSONS", learningService.teamWeeklyCompleted]
                    ]
                    Rectangle {
                        required property var modelData
                        Layout.fillWidth: true
                        Layout.preferredHeight: 58
                        radius: 12
                        color: "#10243A"
                        border.color: "#345B67"
                        Column {
                            anchors.centerIn: parent
                            spacing: 2
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: modelData[1]
                                color: "white"
                                font.pixelSize: 16
                                font.bold: true
                            }
                            Text {
                                anchors.horizontalCenter: parent.horizontalCenter
                                text: modelData[0]
                                color: "#7FAAAE"
                                font.pixelSize: 8
                                font.bold: true
                                font.letterSpacing: 0.8
                            }
                        }
                    }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Text {
                    text: "Weekly team goal"
                    color: "#D5E8F3"
                    font.pixelSize: 11
                    font.bold: true
                }
                Item { Layout.fillWidth: true }
                Text {
                    text: learningService.teamWeeklyCompleted + " / " + learningService.teamWeeklyGoal
                    color: "#68EDC6"
                    font.pixelSize: 11
                    font.bold: true
                }
            }
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 8
                radius: 4
                color: "#24334B"
                Rectangle {
                    width: parent.width * learningService.teamWeeklyCompleted / learningService.teamWeeklyGoal
                    height: parent.height
                    radius: parent.radius
                    gradient: Gradient {
                        GradientStop { position: 0; color: "#1B9A83" }
                        GradientStop { position: 1; color: "#5B6EE1" }
                    }
                }
            }
            Text {
                text: "WEEKLY CONTRIBUTORS"
                color: "#7FAAAE"
                font.pixelSize: 9
                font.bold: true
                font.letterSpacing: 1.1
            }
            ListView {
                id: teamMemberList
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 4
                model: learningService.teamMemberItems
                delegate: Rectangle {
                    required property string modelData
                    property var fields: modelData.split("|")
                    width: teamMemberList.width
                    height: 42
                    radius: 11
                    color: fields[0].indexOf("(You)") >= 0 ? "#183954" : "#101D34"
                    border.color: fields[0].indexOf("(You)") >= 0 ? "#4FAF9F" : "#354761"
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 7
                        Rectangle {
                            Layout.preferredWidth: 26
                            Layout.preferredHeight: 26
                            radius: 13
                            color: "#24526A"
                            Text {
                                anchors.centerIn: parent
                                text: fields[0].charAt(0)
                                color: "#CFF7F0"
                                font.bold: true
                            }
                        }
                        Column {
                            Layout.fillWidth: true
                            spacing: 1
                            Text { text: fields[0]; color: "#EFF5FF"; font.pixelSize: 11; font.bold: true }
                            Text { text: fields[1]; color: "#8FA5C2"; font.pixelSize: 9 }
                        }
                        Column {
                            spacing: 1
                            Text { anchors.right: parent.right; text: fields[3]; color: "#68EDC6"; font.pixelSize: 10; font.bold: true }
                            Text { anchors.right: parent.right; text: fields[2]; color: "#8FA5C2"; font.pixelSize: 9 }
                        }
                    }
                }
            }
            Text {
                Layout.fillWidth: true
                text: "Sample data • ready for team identity and shared sync"
                color: "#758CA9"
                font.pixelSize: 9
                horizontalAlignment: Text.AlignHCenter
            }
            Button {
                Layout.fillWidth: true
                Layout.preferredHeight: 38
                text: "Close Team Board"
                onClicked: teamBoardPopup.close()
            }
        }
    }

    Popup {
        id: goalPopup
        objectName: "goalPopup"
        anchors.centerIn: Overlay.overlay
        width: 360
        height: 440
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 24

        onOpened: {
            const selected = learningService.learningGoals.indexOf(learningService.learningGoal)
            goalPicker.currentIndex = selected >= 0 ? selected : 0
            goalPicker.forceActiveFocus()
        }

        background: Rectangle {
            radius: 26
            border.width: 1
            border.color: "#3B8D86"
            gradient: Gradient {
                GradientStop { position: 0; color: "#17343F" }
                GradientStop { position: 1; color: "#11172F" }
            }
        }

        contentItem: ColumnLayout {
            spacing: 12
            Text {
                Layout.fillWidth: true
                text: "LEARNING GOAL"
                color: "#68EDC6"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 1.5
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                Layout.fillWidth: true
                text: "Choose a curated path. FlashTile sequences approved lessons locally—no personal data or AI prompt is sent anywhere."
                color: "#B7C7E1"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            ComboBox {
                id: goalPicker
                Layout.fillWidth: true
                model: learningService.learningGoals
                Accessible.name: "Guided learning path"
            }
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: goalDescription.implicitHeight + 22
                radius: 12
                color: "#10243A"
                border.color: "#345B67"
                Text {
                    id: goalDescription
                    anchors.fill: parent
                    anchors.margins: 11
                    text: learningService.describeLearningGoal(goalPicker.currentText)
                    color: "#D5E8F3"
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                }
            }
            Text {
                visible: learningService.goalActive
                Layout.fillWidth: true
                text: "Current: " + learningService.learningGoal + " • " + learningService.goalProgressText
                color: "#8FDACD"
                font.pixelSize: 11
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            CheckBox {
                Layout.fillWidth: true
                text: "Reduce decorative motion"
                checked: learningService.reducedMotion
                Accessible.name: "Reduce decorative motion"
                indicator: Rectangle {
                    implicitWidth: 24
                    implicitHeight: 24
                    x: parent.leftPadding
                    y: parent.height / 2 - height / 2
                    radius: 6
                    color: parent.checked ? "#1B9A83" : "#10243A"
                    border.color: parent.activeFocus ? "#8FF5E0" : "#4E7D84"
                    Text {
                        anchors.centerIn: parent
                        text: "✓"
                        visible: parent.parent.checked
                        color: "white"
                        font.bold: true
                    }
                }
                contentItem: Text {
                    text: parent.text
                    color: "#D5E8F3"
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    leftPadding: parent.indicator.width + parent.spacing
                }
                onToggled: {
                    learningService.setReducedMotion(checked)
                    if (checked) {
                        heroCard.tiltX = 0
                        heroCard.tiltY = 0
                    }
                }
            }
            Item { Layout.fillHeight: true }
            Button {
                visible: learningService.goalActive
                Layout.fillWidth: true
                Layout.preferredHeight: 38
                text: "Stop current guided path"
                onClicked: {
                    learningService.clearLearningGoal()
                    goalPopup.close()
                }
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 9
                Button {
                    Layout.preferredWidth: 86
                    Layout.preferredHeight: 42
                    text: "Cancel"
                    onClicked: goalPopup.close()
                }
                Button {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 42
                    text: learningService.goalActive ? "Start selected path" : "Start guided path"
                    onClicked: {
                        learningService.selectLearningGoal(goalPicker.currentText)
                        flowStep = 0
                        selectedAnswer = -1
                        feedbackText = "Guided path started."
                        feedbackColor = "#68EDC6"
                        goalPopup.close()
                    }
                    background: Rectangle {
                        radius: 13
                        opacity: parent.enabled ? 1 : 0.45
                        gradient: Gradient {
                            GradientStop { position: 0; color: "#1B9A83" }
                            GradientStop { position: 1; color: "#4B67D1" }
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
        id: discoveryPopup
        objectName: "discoveryPopup"
        anchors.centerIn: Overlay.overlay
        width: 360
        height: 380
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 24

        background: Rectangle {
            radius: 26
            border.width: 1
            border.color: "#8A713B"
            gradient: Gradient {
                GradientStop { position: 0; color: "#322819" }
                GradientStop { position: 0.38; color: "#17243A" }
                GradientStop { position: 1; color: "#11172F" }
            }
        }

        contentItem: ColumnLayout {
            spacing: 12
            Text {
                Layout.fillWidth: true
                text: "DAILY DISCOVERY"
                color: "#FFCB68"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 1.5
                horizontalAlignment: Text.AlignHCenter
            }
            RowLayout {
                Layout.fillWidth: true
                Text {
                    text: learningService.dailyDiscoveryCategory.toUpperCase()
                    color: "#83E8FF"
                    font.pixelSize: 10
                    font.bold: true
                    font.letterSpacing: 1.0
                }
                Item { Layout.fillWidth: true }
                Text {
                    text: learningService.dailyDiscoveryDate
                    color: "#AFC1DD"
                    font.pixelSize: 11
                }
            }
            Text {
                Layout.fillWidth: true
                text: learningService.dailyDiscoveryTitle
                color: "white"
                font.pixelSize: 22
                font.bold: true
                wrapMode: Text.WordWrap
            }
            Text {
                Layout.fillWidth: true
                text: learningService.dailyDiscoveryBody
                color: "#DCE8F8"
                font.pixelSize: 13
                lineHeight: 1.22
                wrapMode: Text.WordWrap
            }
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: discoveryContext.implicitHeight + 22
                radius: 12
                color: "#172A49"
                border.color: "#4B6280"
                Text {
                    id: discoveryContext
                    anchors.fill: parent
                    anchors.margins: 11
                    text: "Why it matters: " + learningService.dailyDiscoveryContext
                    color: "#BCE0F6"
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                }
            }
            Item { Layout.fillHeight: true }
            Text {
                Layout.fillWidth: true
                text: "Curated offline • changes daily"
                color: "#7F96B8"
                font.pixelSize: 10
                horizontalAlignment: Text.AlignHCenter
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 9
                Button {
                    Layout.preferredWidth: 88
                    Layout.preferredHeight: 42
                    text: "Close"
                    onClicked: discoveryPopup.close()
                }
                Button {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 42
                    text: "Show another  →"
                    Accessible.name: "Show another daily discovery"
                    onClicked: learningService.nextDiscovery()
                    background: Rectangle {
                        radius: 13
                        gradient: Gradient {
                            GradientStop { position: 0; color: "#D98B24" }
                            GradientStop { position: 1; color: "#6A55D6" }
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
            Button {
                Layout.fillWidth: true
                Layout.preferredHeight: 34
                text: learningService.noteCount === 0
                    ? "No saved takeaways yet"
                    : "Browse saved takeaways • " + learningService.noteCount
                enabled: learningService.noteCount > 0
                Accessible.name: "Browse all saved learning takeaways"
                onClicked: {
                    notesPopup.close()
                    takeawaysPopup.open()
                }
            }
            TextArea {
                id: noteEditor
                Layout.fillWidth: true
                Layout.preferredHeight: 112
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
                        opacity: parent.enabled ? 1 : 0.45
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
        id: takeawaysPopup
        objectName: "takeawaysPopup"
        anchors.centerIn: Overlay.overlay
        width: 360
        height: 440
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape
        padding: 22

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
            spacing: 10
            Text {
                Layout.fillWidth: true
                text: "SAVED TAKEAWAYS"
                color: "#B8AFFF"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 1.5
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                Layout.fillWidth: true
                text: "Open a takeaway to return to its lesson and continue editing."
                color: "#B7C7E1"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            Text {
                visible: learningService.noteCount === 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                text: "No saved takeaways yet."
                color: "#8192AE"
                font.pixelSize: 12
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            ListView {
                id: takeawayList
                visible: learningService.noteCount > 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                spacing: 7
                model: learningService.noteItems
                delegate: Rectangle {
                    required property int index
                    required property string modelData
                    width: takeawayList.width
                    height: 64
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
                            Accessible.name: "Open saved takeaway " + modelData
                            onClicked: {
                                learningService.openNote(index)
                                takeawaysPopup.close()
                                notesPopup.open()
                                flowStep = 0
                                selectedAnswer = -1
                                feedbackText = "Saved takeaway opened."
                                feedbackColor = "#B8AFFF"
                            }
                            contentItem: Text {
                                text: parent.text
                                color: "#EAF3FF"
                                font.pixelSize: 11
                                maximumLineCount: 2
                                elide: Text.ElideRight
                                wrapMode: Text.WordWrap
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                        Button {
                            Layout.preferredWidth: 34
                            Layout.fillHeight: true
                            flat: true
                            text: "×"
                            Accessible.name: "Remove saved takeaway"
                            onClicked: learningService.removeNote(index)
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
                onClicked: takeawaysPopup.close()
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
                        running: resetTimer.running && !learningService.reducedMotion
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

    Shortcut {
        sequence: "Ctrl+G"
        onActivated: goalPopup.open()
    }

    Shortcut {
        sequence: "Ctrl+B"
        onActivated: bookmarksPopup.open()
    }

    Shortcut {
        sequence: "Ctrl+N"
        onActivated: notesPopup.open()
    }

    Shortcut {
        sequence: "Ctrl+D"
        onActivated: discoveryPopup.open()
    }

    Shortcut {
        sequence: "Ctrl+T"
        onActivated: teamBoardPopup.open()
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

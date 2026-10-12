from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>TypeSpeed</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #0b0f0e;
            color: white;
            min-height: 100vh;

            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            width: 90%;
            max-width: 900px;
        }


        /* =========================
           HEADER
        ========================= */

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;

            margin-bottom: 30px;
        }

        .logo {
            font-size: 28px;
            font-weight: bold;
        }

        .online {
            color: #39ff88;
            font-size: 14px;
        }

        .online::before {
            content: "";

            display: inline-block;

            width: 8px;
            height: 8px;

            background: #39ff88;

            border-radius: 50%;

            margin-right: 7px;
        }


        /* =========================
           TIMER
        ========================= */

        .timer-box {
            text-align: center;
            margin-bottom: 25px;
        }

        #timer {
            font-size: 55px;
            font-weight: bold;
            color: #39ff88;
        }


        /* =========================
           TIME BUTTONS
        ========================= */

        .time-buttons {
            display: flex;
            justify-content: center;

            gap: 10px;

            margin-top: 15px;
        }

        .time-buttons button {
            background: #151b19;
            color: white;

            border: 1px solid #303a36;

            padding: 10px 18px;

            border-radius: 8px;

            cursor: pointer;

            transition: 0.2s;
        }

        .time-buttons button:hover {
            border-color: #39ff88;
        }

        .time-buttons button.active {
            background: #39ff88;
            color: #07100b;

            font-weight: bold;
        }


        /* =========================
           STATS
        ========================= */

        .stats {
            display: flex;
            justify-content: center;

            gap: 50px;

            margin-bottom: 25px;

            color: #aaa;
        }

        .stats span {
            color: white;
            font-weight: bold;
        }


        /* =========================
           TYPING AREA
        ========================= */

        .typing-area {
            background: #111715;

            border: 1px solid #26302c;

            border-radius: 15px;

            padding: 30px;
        }

        #text {
            font-size: 22px;

            line-height: 1.8;

            color: #777;

            min-height: 160px;

            margin-bottom: 25px;

            word-wrap: break-word;
        }

        .correct {
            color: #39ff88;
        }

        .wrong {
            color: #ff4d5a;

            text-decoration: underline;
        }

        .current {
            border-left: 2px solid #39ff88;
        }


        textarea {
            width: 100%;

            height: 100px;

            resize: none;

            background: #0b0f0e;

            border: 1px solid #303a36;

            border-radius: 10px;

            color: white;

            padding: 15px;

            font-size: 18px;

            outline: none;
        }

        textarea:focus {
            border-color: #39ff88;
        }


        .restart {
            margin-top: 20px;

            width: 100%;

            padding: 13px;

            border: none;

            border-radius: 9px;

            background: #39ff88;

            color: #07100b;

            font-size: 16px;

            font-weight: bold;

            cursor: pointer;
        }

        .restart:hover {
            opacity: 0.85;
        }


        /* =========================
           POPUP OVERLAY
        ========================= */

        .popup-overlay {

            position: fixed;

            inset: 0;

            background: rgba(0, 0, 0, 0.78);

            display: none;

            justify-content: center;
            align-items: center;

            z-index: 1000;

            backdrop-filter: blur(6px);
        }


        /* =========================
           POPUP
        ========================= */

        .popup {

            width: 90%;

            max-width: 500px;

            background: #111715;

            border: 2px solid #303a36;

            border-radius: 20px;

            padding: 35px;

            text-align: center;

            box-shadow:
                0 20px 70px rgba(0,0,0,0.7);

            animation: popupIn 0.3s ease;

            transition:
                background 0.3s,
                border-color 0.3s,
                box-shadow 0.3s;
        }


        @keyframes popupIn {

            from {
                transform: scale(0.8);
                opacity: 0;
            }

            to {
                transform: scale(1);
                opacity: 1;
            }

        }


        /* =========================
           LOW RESULT
        ========================= */

        .popup.low {

            background:
                linear-gradient(
                    145deg,
                    #351010,
                    #1a0b0b
                );

            border-color: #ff3b3b;

            box-shadow:
                0 0 40px rgba(255, 50, 50, 0.35);
        }


        /* =========================
           MEDIUM RESULT
        ========================= */

        .popup.medium {

            background:
                linear-gradient(
                    145deg,
                    #3a3008,
                    #1b1707
                );

            border-color: #ffd43b;

            box-shadow:
                0 0 40px rgba(255, 210, 50, 0.35);
        }


        /* =========================
           HIGH RESULT
        ========================= */

        .popup.high {

            background:
                linear-gradient(
                    145deg,
                    #083a20,
                    #071c12
                );

            border-color: #39ff88;

            box-shadow:
                0 0 45px rgba(57, 255, 136, 0.4);
        }


        .result-icon {

            font-size: 55px;

            margin-bottom: 8px;
        }


        .popup h2 {

            font-size: 30px;

            margin-bottom: 8px;
        }


        .popup-subtitle {

            color: #aaa;

            margin-bottom: 25px;
        }


        .result-main {

            margin-bottom: 25px;
        }


        .result-wpm {

            font-size: 65px;

            font-weight: bold;

            color: #39ff88;
        }


        .popup.low .result-wpm {
            color: #ff4d4d;
        }

        .popup.medium .result-wpm {
            color: #ffd43b;
        }

        .popup.high .result-wpm {
            color: #39ff88;
        }


        .wpm-label {

            color: #888;

            font-size: 14px;
        }


        /* =========================
           RESULT GRID
        ========================= */

        .result-grid {

            display: grid;

            grid-template-columns:
                1fr 1fr;

            gap: 12px;

            margin-top: 25px;
        }


        .result-card {

            background: rgba(0,0,0,0.25);

            border: 1px solid #252e2b;

            border-radius: 12px;

            padding: 18px 10px;
        }


        .result-card .value {

            font-size: 24px;

            font-weight: bold;

            margin-bottom: 5px;
        }


        .result-card .label {

            color: #888;

            font-size: 13px;
        }


        /* =========================
           BUTTON
        ========================= */

        .popup-button {

            margin-top: 25px;

            width: 100%;

            padding: 14px;

            background: #39ff88;

            color: #07100b;

            border: none;

            border-radius: 10px;

            font-size: 16px;

            font-weight: bold;

            cursor: pointer;
        }


        .popup.low .popup-button {
            background: #ff4d4d;
            color: white;
        }

        .popup.medium .popup-button {
            background: #ffd43b;
            color: #171300;
        }

        .popup.high .popup-button {
            background: #39ff88;
            color: #07100b;
        }


        .popup-button:hover {
            opacity: 0.85;
        }


        /* =========================
           MOBILE
        ========================= */

        @media (max-width: 600px) {

            #text {
                font-size: 18px;
            }

            .stats {
                gap: 20px;
            }

            .result-wpm {
                font-size: 50px;
            }

        }

    </style>

</head>


<body>


<div class="container">


    <div class="header">

        <div class="logo">
            TypeSpeed
        </div>

        <div class="online">
            ONLINE
        </div>

    </div>


    <div class="timer-box">

        <div id="timer">
            10
        </div>


        <div class="time-buttons">

            <button
                id="btn10"
                onclick="selectTime(10)"
            >
                10 Seconds
            </button>


            <button
                id="btn30"
                onclick="selectTime(30)"
            >
                30 Seconds
            </button>


            <button
                id="btn60"
                onclick="selectTime(60)"
            >
                1 Minute
            </button>

        </div>

    </div>


    <div class="stats">

        <div>
            WPM:
            <span id="wpm">
                0
            </span>
        </div>


        <div>
            Accuracy:
            <span id="accuracy">
                100
            </span>%
        </div>


        <div>
            Errors:
            <span id="errors">
                0
            </span>
        </div>

    </div>


    <div class="typing-area">

        <div id="text"></div>


        <textarea
            id="input"
            placeholder="Start typing here..."
            spellcheck="false"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
        ></textarea>


        <button
            class="restart"
            onclick="restart()"
        >
            Restart Test
        </button>

    </div>

</div>



<!-- =========================
     RESULT POPUP
========================= -->

<div
    class="popup-overlay"
    id="popup"
>

    <div
        class="popup"
        id="popupBox"
    >


        <div
            class="result-icon"
            id="resultIcon"
        >
            🎉
        </div>


        <h2 id="resultTitle">
            Test Complete!
        </h2>


        <div
            class="popup-subtitle"
            id="resultSubtitle"
        >
            Here's your typing result
        </div>


        <div class="result-main">

            <div
                class="result-wpm"
                id="finalWpm"
            >
                0
            </div>


            <div class="wpm-label">
                WORDS PER MINUTE
            </div>

        </div>


        <div class="result-grid">


            <div class="result-card">

                <div
                    class="value"
                    id="finalAccuracy"
                >
                    0%
                </div>

                <div class="label">
                    Accuracy
                </div>

            </div>


            <div class="result-card">

                <div
                    class="value"
                    id="finalErrors"
                >
                    0
                </div>

                <div class="label">
                    Errors
                </div>

            </div>


            <div class="result-card">

                <div
                    class="value"
                    id="finalCharacters"
                >
                    0
                </div>

                <div class="label">
                    Characters
                </div>

            </div>


            <div class="result-card">

                <div
                    class="value"
                    id="finalTime"
                >
                    0s
                </div>

                <div class="label">
                    Time
                </div>

            </div>

        </div>


        <button
            class="popup-button"
            onclick="closePopupAndRestart()"
        >
            Try Again
        </button>


    </div>

</div>



<script>


/* ==========================================
   TEXT DATABASE
========================================== */

const texts = [

    "The quick brown fox jumps over the lazy dog. Typing speed is not only about going fast, but also about maintaining accuracy and consistency. Practice every day and your typing speed will improve.",

    "Technology continues to change the way people work, communicate, and learn. Good typing skills can help you write faster, stay focused, and spend less time correcting simple mistakes.",

    "A great typing session is all about rhythm, accuracy, and consistency. Do not rush every single word. Keep your hands relaxed, watch the screen, and let your fingers become more comfortable with every practice session."

];


let currentText = "";

let lastTextIndex = -1;

let selectedTime = 10;

let remainingTime = 10;

let started = false;

let finished = false;

let timer = null;

let startTime = null;


/* ==========================================
   ELEMENTS
========================================== */

const textElement =
    document.getElementById("text");

const inputElement =
    document.getElementById("input");

const popup =
    document.getElementById("popup");

const popupBox =
    document.getElementById("popupBox");


/* ==========================================
   RANDOM TEXT
========================================== */

function getRandomText() {

    let randomIndex;


    do {

        randomIndex =
            Math.floor(
                Math.random() * texts.length
            );

    } while (
        randomIndex === lastTextIndex &&
        texts.length > 1
    );


    lastTextIndex =
        randomIndex;


    currentText =
        texts[randomIndex];

}


/* ==========================================
   SELECT TIME
========================================== */

function selectTime(seconds) {

    selectedTime = seconds;

    restart();

}


/* ==========================================
   TIME BUTTONS
========================================== */

function updateTimeButtons() {

    document
        .getElementById("btn10")
        .classList.remove("active");

    document
        .getElementById("btn30")
        .classList.remove("active");

    document
        .getElementById("btn60")
        .classList.remove("active");


    if (selectedTime === 10) {

        document
            .getElementById("btn10")
            .classList.add("active");

    }


    if (selectedTime === 30) {

        document
            .getElementById("btn30")
            .classList.add("active");

    }


    if (selectedTime === 60) {

        document
            .getElementById("btn60")
            .classList.add("active");

    }

}


/* ==========================================
   RENDER TEXT
========================================== */

function renderText() {

    const typed =
        inputElement.value;

    let html = "";


    for (
        let i = 0;
        i < currentText.length;
        i++
    ) {

        const char =
            currentText[i];


        if (i < typed.length) {

            if (
                typed[i] === char
            ) {

                html +=
                    `<span class="correct">
                        ${escapeHTML(char)}
                    </span>`;

            }

            else {

                html +=
                    `<span class="wrong">
                        ${escapeHTML(char)}
                    </span>`;

            }

        }


        else if (
            i === typed.length
        ) {

            html +=
                `<span class="current">
                    ${escapeHTML(char)}
                </span>`;

        }


        else {

            html +=
                escapeHTML(char);

        }

    }


    textElement.innerHTML =
        html;

}


/* ==========================================
   ESCAPE HTML
========================================== */

function escapeHTML(char) {

    return char
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");

}


/* ==========================================
   INPUT
========================================== */

inputElement.addEventListener(
    "input",
    function() {

        if (finished)
            return;


        if (
            !started &&
            inputElement.value.length > 0
        ) {

            started = true;

            startTime =
                Date.now();


            timer =
                setInterval(
                    countdown,
                    100
                );

        }


        renderText();

        updateStats();

    }
);


/* ==========================================
   COUNTDOWN
========================================== */

function countdown() {

    const elapsed =
        (Date.now() - startTime) / 1000;


    remainingTime =
        Math.max(
            0,
            selectedTime - elapsed
        );


    document
        .getElementById("timer")
        .textContent =
        Math.ceil(remainingTime);


    updateStats();


    if (
        remainingTime <= 0
    ) {

        finishTest();

    }

}


/* ==========================================
   GET STATS
========================================== */

function getStats() {

    const typed =
        inputElement.value;


    let correct = 0;


    for (
        let i = 0;
        i < typed.length;
        i++
    ) {

        if (
            typed[i] === currentText[i]
        ) {

            correct++;

        }

    }


    const errors =
        typed.length - correct;


    let elapsedSeconds =
        selectedTime - remainingTime;


    if (!started) {

        elapsedSeconds = 0;

    }


    if (finished) {

        elapsedSeconds =
            selectedTime;

    }


    const minutes =
        elapsedSeconds / 60;


    let wpm = 0;


    if (minutes > 0) {

        wpm =
            (correct / 5) /
            minutes;

    }


    let accuracy = 100;


    if (typed.length > 0) {

        accuracy =
            (correct /
            typed.length) *
            100;

    }


    return {

        typed:
            typed.length,

        correct:
            correct,

        errors:
            errors,

        wpm:
            wpm,

        accuracy:
            accuracy,

        time:
            elapsedSeconds

    };

}


/* ==========================================
   UPDATE LIVE STATS
========================================== */

function updateStats() {

    const stats =
        getStats();


    document
        .getElementById("wpm")
        .textContent =
        Math.round(stats.wpm);


    document
        .getElementById("accuracy")
        .textContent =
        Math.round(stats.accuracy);


    document
        .getElementById("errors")
        .textContent =
        stats.errors;

}


/* ==========================================
   SOUND ENGINE
========================================== */

let audioContext = null;


function getAudioContext() {

    if (!audioContext) {

        audioContext =
            new (
                window.AudioContext ||
                window.webkitAudioContext
            )();

    }


    if (
        audioContext.state === "suspended"
    ) {

        audioContext.resume();

    }


    return audioContext;

}


/* ==========================================
   PLAY TONE
========================================== */

function playTone(
    frequency,
    duration,
    delay = 0,
    type = "sine",
    volume = 0.12
) {

    const ctx =
        getAudioContext();


    const oscillator =
        ctx.createOscillator();


    const gain =
        ctx.createGain();


    oscillator.type =
        type;


    oscillator.frequency.value =
        frequency;


    gain.gain.setValueAtTime(
        0,
        ctx.currentTime + delay
    );


    gain.gain.linearRampToValueAtTime(
        volume,
        ctx.currentTime + delay + 0.01
    );


    gain.gain.exponentialRampToValueAtTime(
        0.001,
        ctx.currentTime +
        delay +
        duration
    );


    oscillator.connect(gain);

    gain.connect(ctx.destination);


    oscillator.start(
        ctx.currentTime + delay
    );


    oscillator.stop(
        ctx.currentTime +
        delay +
        duration
    );

}


/* ==========================================
   LOW SOUND
   "NGELEDEK"
========================================== */

function playLowSound() {

    const ctx =
        getAudioContext();


    // Sad descending tones

    playTone(
        220,
        0.25,
        0,
        "sawtooth",
        0.10
    );


    playTone(
        180,
        0.25,
        0.20,
        "sawtooth",
        0.10
    );


    playTone(
        130,
        0.45,
        0.40,
        "sawtooth",
        0.10
    );


    // Small comedic beep

    playTone(
        100,
        0.18,
        0.90,
        "square",
        0.07
    );

}


/* ==========================================
   MEDIUM SOUND
   APPLAUSE
========================================== */

function playMediumSound() {

    // Small success melody

    playTone(
        440,
        0.18,
        0,
        "sine",
        0.10
    );


    playTone(
        520,
        0.18,
        0.15,
        "sine",
        0.10
    );


    playTone(
        660,
        0.25,
        0.30,
        "sine",
        0.12
    );


    // Applause simulation

    for (
        let i = 0;
        i < 18;
        i++
    ) {

        const delay =
            0.45 +
            Math.random() * 1.3;


        playTone(
            700 +
            Math.random() * 900,
            0.025,
            delay,
            "square",
            0.025
        );

    }

}


/* ==========================================
   HIGH SOUND
   CHEER + APPLAUSE
========================================== */

function playHighSound() {

    // Victory melody

    playTone(
        523,
        0.18,
        0,
        "sine",
        0.12
    );


    playTone(
        659,
        0.18,
        0.15,
        "sine",
        0.12
    );


    playTone(
        784,
        0.18,
        0.30,
        "sine",
        0.12
    );


    playTone(
        1047,
        0.45,
        0.45,
        "sine",
        0.14
    );


    // Big applause

    for (
        let i = 0;
        i < 40;
        i++
    ) {

        const delay =
            0.75 +
            Math.random() * 2.0;


        playTone(
            600 +
            Math.random() * 1300,
            0.025,
            delay,
            "square",
            0.035
        );

    }


    // Cheer-like rising notes

    playTone(
        700,
        0.15,
        0.8,
        "sawtooth",
        0.04
    );


    playTone(
        900,
        0.15,
        0.95,
        "sawtooth",
        0.04
    );


    playTone(
        1200,
        0.30,
        1.1,
        "sawtooth",
        0.04
    );

}


/* ==========================================
   DETERMINE RESULT
========================================== */

function getResultLevel(
    wpm,
    accuracy
) {

    /*
        HIGH:
        WPM >= 50
        AND Accuracy >= 95

        MEDIUM:
        WPM >= 30
        AND Accuracy >= 80

        LOW:
        Anything below that
    */


    if (
        wpm >= 50 &&
        accuracy >= 95
    ) {

        return "high";

    }


    if (
        wpm >= 30 &&
        accuracy >= 80
    ) {

        return "medium";

    }


    return "low";

}


/* ==========================================
   SHOW RESULT
========================================== */

function showResult(
    stats
) {

    const wpm =
        Math.round(stats.wpm);


    const accuracy =
        Math.round(stats.accuracy);


    const level =
        getResultLevel(
            wpm,
            accuracy
        );


    // Remove old classes

    popupBox.classList.remove(
        "low",
        "medium",
        "high"
    );


    // Add new class

    popupBox.classList.add(
        level
    );


    if (level === "low") {

        document
            .getElementById("resultIcon")
            .textContent =
            "💀";


        document
            .getElementById("resultTitle")
            .textContent =
            "Bro... 💀";


        document
            .getElementById("resultSubtitle")
            .textContent =
            "Your keyboard is waiting for you to wake up.";


        playLowSound();

    }


    else if (level === "medium") {

        document
            .getElementById("resultIcon")
            .textContent =
            "👏";


        document
            .getElementById("resultTitle")
            .textContent =
            "Not Bad! 👏";


        document
            .getElementById("resultSubtitle")
            .textContent =
            "Solid typing! Keep practicing.";


        playMediumSound();

    }


    else {

        document
            .getElementById("resultIcon")
            .textContent =
            "🏆";


        document
            .getElementById("resultTitle")
            .textContent =
            "LET'S GOOO! 🔥";


        document
            .getElementById("resultSubtitle")
            .textContent =
            "That's some seriously fast typing!";


        playHighSound();

    }


    // Fill result

    document
        .getElementById("finalWpm")
        .textContent =
        wpm;


    document
        .getElementById("finalAccuracy")
        .textContent =
        accuracy + "%";


    document
        .getElementById("finalErrors")
        .textContent =
        stats.errors;


    document
        .getElementById("finalCharacters")
        .textContent =
        stats.typed;


    document
        .getElementById("finalTime")
        .textContent =
        selectedTime + "s";


    // Show popup

    popup.style.display =
        "flex";

}


/* ==========================================
   FINISH TEST
========================================== */

function finishTest() {

    if (finished)
        return;


    finished = true;


    clearInterval(timer);


    inputElement.disabled =
        true;


    remainingTime = 0;


    document
        .getElementById("timer")
        .textContent =
        "0";


    const stats =
        getStats();


    showResult(stats);

}


/* ==========================================
   CLOSE POPUP
========================================== */

function closePopupAndRestart() {

    popup.style.display =
        "none";


    restart();

}


/* ==========================================
   RESTART
========================================== */

function restart() {

    clearInterval(timer);


    started = false;

    finished = false;


    remainingTime =
        selectedTime;


    inputElement.disabled =
        false;


    inputElement.value =
        "";


    document
        .getElementById("timer")
        .textContent =
        selectedTime;


    getRandomText();


    updateTimeButtons();

    updateStats();

    renderText();


    inputElement.focus();

}


/* ==========================================
   INITIAL
========================================== */

selectTime(10);

</script>


</body>

</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


if __name__ == "__main__":

    print("=" * 50)
    print("TypeSpeed Server")
    print("Local:   http://127.0.0.1:5000")
    print("Network: http://YOUR-IP:5000")
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
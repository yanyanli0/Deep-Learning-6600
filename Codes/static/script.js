// static/script.js
let countdownInterval;

function startCountdown(duration) {
    let timer = duration, minutes, seconds;
    countdownInterval = setInterval(() => {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        document.getElementById('countdown').textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
            clearInterval(countdownInterval);
            document.getElementById('countdown').textContent = '';
        }
    }, 1000);
}

function record() {
    startCountdown(30);
    // AJAX request to trigger recording on the server
    fetch('/record', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log(data.status));
}

// script.js
function play() {
    let playButton = document.getElementById('playButton');
    playButton.disabled = true;

    fetch('/play', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            playButton.disabled = false;
        });
}

// function play() {
//     // AJAX request to trigger playback on the server
//     fetch('/play', { method: 'GET' })
//         .then(response => response.json())
//         .then(data => console.log(data.status));
// }

function transcribe() {
    // AJAX request to trigger transcription on the server
    fetch('/transcribe', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.transcription) {
                document.getElementById("transcription").value = data.transcription;
            } else {
                console.error("Transcription file not found");
            }
        });
}

function correctText() {
    fetch('/correct_text', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.corrected_text) {
                document.getElementById("corrected_text").value = data.corrected_text;
            } else {
                console.error("Corrected text file not found");
            }
        });
}
// Additional JavaScript code for handling UI interactions

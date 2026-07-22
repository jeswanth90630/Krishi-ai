function startVoice() {
    const recognition = new webkitSpeechRecognition();
    recognition.start();

    recognition.onresult = function(event) {
        const command = event.results[0][0].transcript;

        if(command.includes("detect")) {
            window.location.href = "detection.html";
        }
    }
}
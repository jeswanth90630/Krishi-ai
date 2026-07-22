function startDetection() {
    window.location.href = "detection.html";
}

// Live time using Luxon
const DateTime = luxon.DateTime;

setInterval(() => {
    const now = DateTime.now().toFormat("hh:mm a");
    console.log("Time:", now);
}, 1000);
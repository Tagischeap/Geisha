const socket = io();

const canvas = document.getElementById("drawingCanvas");
const ctx = canvas.getContext("2d");
let drawing = false;

// Start drawing when mouse is pressed
canvas.addEventListener("mousedown", () => drawing = true);
canvas.addEventListener("mouseup", () => drawing = false);
canvas.addEventListener("mouseout", () => drawing = false);

// Send drawing data when mouse is moved
canvas.addEventListener("mousemove", (event) => {
    if (!drawing) return;

    const pos = { x: event.offsetX, y: event.offsetY };
    socket.emit("draw", pos); // Send draw event to the server

    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
});

// Receive drawing updates from server
socket.on("draw", (pos) => {
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
});

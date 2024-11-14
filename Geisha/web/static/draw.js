// web/static/draw.js
const socket = io();
const canvas = document.getElementById("drawingCanvas");
const ctx = canvas.getContext("2d");
let drawing = false;
const lobbyId = window.location.pathname.split("/").pop();

socket.emit("join_lobby", { lobby_id: lobbyId, username: "defaultUser" });

// Configure the canvas drawing settings
ctx.strokeStyle = "black";
ctx.lineWidth = 2;

// Start drawing a new path when mouse is pressed
canvas.addEventListener("mousedown", (event) => {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(event.offsetX, event.offsetY);
    socket.emit("draw_start", { lobby_id: lobbyId, pos: { x: event.offsetX, y: event.offsetY } });
});

canvas.addEventListener("mouseup", () => drawing = false);
canvas.addEventListener("mouseout", () => drawing = false);

// Draw and send data as the mouse moves
canvas.addEventListener("mousemove", (event) => {
    if (!drawing) return;

    const pos = { x: event.offsetX, y: event.offsetY };
    socket.emit("draw", { lobby_id: lobbyId, pos });
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
});

// Helper functions to process historical events
function startDrawing(pos) {
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function continueDrawing(pos) {
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

// Updated drawing history listener
socket.on('drawing_history', (data) => {
    console.log("Received drawing history:", data.history); // Debugging log
    data.history.forEach(event => {
        if (event.type === 'draw_start') {
            startDrawing(event.data.pos);
        } else if (event.type === 'draw') {
            continueDrawing(event.data.pos);
        }
    });
});


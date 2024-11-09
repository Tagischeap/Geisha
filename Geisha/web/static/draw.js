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

socket.on("draw_start", (data) => {
    console.log("Received draw_start event:", data); // Debugging log
    ctx.beginPath();
    ctx.moveTo(data.pos.x, data.pos.y);
});

socket.on("draw", (data) => {
    console.log("Received draw event:", data); // Debugging log
    ctx.lineTo(data.pos.x, data.pos.y);
    ctx.stroke();
});

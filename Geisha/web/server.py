from flask import Flask, render_template, request
import base64
import discord
import asyncio

# Initialize Flask app
app = Flask(__name__)

# Function to send the drawing to Discord
async def send_drawing_to_discord(drawing_path):
    from main import client  # Import the client here to avoid circular dependency
    channel = client.get_channel(601259969601339402)  # Replace with your actual channel ID

    if channel is None:
        print(f"Channel not found with ID: {601259969601339402}")
        print("Available guilds and channels:")
        for guild in client.guilds:
            print(f"Guild: {guild.name} (ID: {guild.id})")
            for channel in guild.channels:
                print(f"  Channel: {channel.name} (ID: {channel.id})")
        return  # Exit if the channel is not found

    with open(drawing_path, "rb") as f:
        discord_file = discord.File(f, filename="drawing.png")
        await channel.send(file=discord_file, content="A new drawing has been submitted!")



@app.route("/draw")
def draw():
    return render_template("draw.html")

@app.route("/submit_drawing", methods=["POST"])
def submit_drawing():
    drawing_data = request.json['drawing']
    header, encoded = drawing_data.split(',', 1)
    data = base64.b64decode(encoded)

    image_path = "drawing.png"  # Change this as needed
    with open(image_path, "wb") as f:
        f.write(data)

    asyncio.run(send_drawing_to_discord(image_path))

    return "Drawing submitted!"

def start_server():
    app.run(host="0.0.0.0", port=8080)

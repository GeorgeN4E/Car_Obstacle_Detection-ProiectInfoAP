from flask import Flask, send_file
from picamera2 import Picamera2, MappedArray
import threading
import time
import os

app = Flask(__name__)

# Configuration
VIDEO_PATH = "/home/pi/latest_video.h264"  # Path to store the video
RECORD_DURATION = 5  # Duration of each video in seconds

# Initialize Picamera2
picam2 = Picamera2()


def record_video_loop():
    """
    Continuously record 5-second video clips, overwriting the same file.
    """
    while True:
        try:
            print(f"Recording video: {VIDEO_PATH}")
            picam2.start_recording(VIDEO_PATH, codec="h264")  # Start recording
            time.sleep(RECORD_DURATION)  # Record for 5 seconds
            picam2.stop_recording()  # Stop recording
            print(f"Video saved to {VIDEO_PATH}")
        except Exception as e:
            print(f"Error during video recording: {e}")


@app.route("/")
def serve_video():
    """
    Serve the most recent 5-second video via the web server.
    """
    if os.path.exists(VIDEO_PATH):
        return send_file(VIDEO_PATH, as_attachment=True, mimetype="video/h264")
    else:
        return "Video not found. Please wait while the camera captures the first clip."


if __name__ == "__main__":
    # Ensure the output folder exists
    os.makedirs(os.path.dirname(VIDEO_PATH), exist_ok=True)

    # Start the video recording thread
    video_thread = threading.Thread(target=record_video_loop, daemon=True)
    video_thread.start()

    # Start the Flask web server
    print("Starting Flask web server on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)

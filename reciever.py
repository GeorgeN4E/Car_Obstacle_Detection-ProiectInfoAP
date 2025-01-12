import subprocess
import os
import time
from PIL import Image
import shutil
import threading
import queue
import keyboard  # For capturing keypresses
from ultralyticsplus import YOLO, render_result

# Initialize directories
captured_directory = 'captured_images'
detected_directory = 'detected_images'

# Clean the captured images directory if it exists
if os.path.exists(captured_directory):
    shutil.rmtree(captured_directory)
else:
    print(f"The directory '{captured_directory}' does not exist.")

# Clean the captured images directory if it exists
if os.path.exists(detected_directory):
    shutil.rmtree(detected_directory)
else:
    print(f"The directory '{detected_directory}' does not exist.")


# Create the output folders if they don't exist
if not os.path.exists(captured_directory):
    os.makedirs(captured_directory)

if not os.path.exists(detected_directory):
    os.makedirs(detected_directory)

# Define the stream input and output parameters
input_stream = 'udp://192.168.168.236:9000'

# Frame capture interval (every 2 seconds)
interval = 2  # seconds

# Initialize the queue for communication between threads
image_queue = queue.Queue()

# Load model
model = YOLO("C:\\Users\\georg\\Downloads\\yolov8s.pt")
# Set model parameters
model.overrides['conf'] = 0.1  # Lower confidence threshold
model.overrides['iou'] = 0.45
model.overrides['agnostic_nms'] = False
model.overrides['max_det'] = 1000

# Function to process image with AI (replace this with your AI function)
def process_image_with_ai(image_path):
    image = Image.open(image_path)
    
    # Perform inference
    results = model.predict(image)

    # Debug output
    print("Bounding Boxes:", results[0].boxes)
    print("Masks:", results[0].masks)

    # Visualize results and save the detected image
    render = render_result(model=model, image=image, result=results[0])
    
    # Create a detected image path
    detected_image_path = os.path.join(detected_directory, os.path.basename(image_path))
    
    # Save the image with detection results
    render.save(detected_image_path)
    
    print(f"Processed and saved: {detected_image_path}")


# Thread for capturing images
def capture_images():
    while not stop_capture_event.is_set():  # Run until capture is stopped
        timestamp = int(time.time())  # Use current timestamp for unique filenames
        output_image_path = f"{captured_directory}/frame_{timestamp}.jpg"

        ffmpeg_command = [
            'ffmpeg',
            '-i', input_stream,
            '-vf', 'fps=1/2',  # Capture one frame every 2 seconds
            '-vframes', '1',  # Only capture one frame
            '-q:v', '2',  # Set image quality (2 is high quality)
            output_image_path  # Save image with a unique name
        ]

        subprocess.run(ffmpeg_command)

        # Put the image path into the queue for processing
        image_queue.put(output_image_path)
        
        time.sleep(interval)

# Thread for processing images
def process_images():
    while not stop_process_event.is_set() or not image_queue.empty():  # Process until stopped and the queue is empty
        if not image_queue.empty():
            image_path = image_queue.get()
            process_image_with_ai(image_path)


# Event objects to handle stopping threads
stop_capture_event = threading.Event()
stop_process_event = threading.Event()

# Start threads
capture_thread = threading.Thread(target=capture_images)
process_thread = threading.Thread(target=process_images)

capture_thread.start()
process_thread.start()

# Handle keypresses to stop threads
try:
    while True:
        if keyboard.is_pressed('q'):  # Stop image capture but let processing continue
            stop_capture_event.set()
            print("Image capture stopped. Processing will continue until finished.")
        
        if keyboard.is_pressed('d'):  # Stop both image capture and processing
            stop_capture_event.set()
            stop_process_event.set()
            print("Stopping everything...")
            break

        time.sleep(0.1)  # Small delay to prevent busy-waiting
finally:
    # Ensure threads are properly joined
    capture_thread.join()
    process_thread.join()
    print("Both threads have finished.")

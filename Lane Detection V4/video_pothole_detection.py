import cv2
import numpy as np
from ultralyticsplus import YOLO, render_result

# Load model
model = YOLO("C:\\Users\\georg\\Downloads\\yolov8s.pt")

# Set model parameters
model.overrides['conf'] = 0.05  # Lower confidence threshold (you can experiment with even lower values)
model.overrides['iou'] = 0.45
model.overrides['agnostic_nms'] = False
model.overrides['max_det'] = 1000

# Load video
video_path = 'Codlea_Brasov.mp4'  # Replace with your actual video file path
cap = cv2.VideoCapture(video_path)

# Check if video was opened successfully
if not cap.isOpened():
    print("Error: Couldn't open video file")
    exit()

# Get the frame rate and dimensions of the video
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize the VideoWriter to save the output
out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("End of video or error reading frame")
        break  # Exit loop if video ends or there's an error reading the frame

    # Perform inference on the current frame
    results = model.predict(frame)

    # Debug output
    print("Bounding Boxes:", results[0].boxes)
    print("Masks:", results[0].masks)

    # Render the result on the frame
    render = render_result(model=model, image=frame, result=results[0])

    # Check if render is valid (not empty or None)
    if render is not None and isinstance(render, np.ndarray):
        # Show the frame with detections
        cv2.imshow('Pothole Detection', render)

        # Write the processed frame to output video
        out.write(render)
    else:
        print("Error: Rendered frame is not valid")

    # Wait for key press; 'q' to quit and save the progress
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to quit and save the progress
        print("Quitting and saving the video...")
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

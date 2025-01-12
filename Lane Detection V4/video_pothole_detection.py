import cv2
from ultralytics import YOLO

# Initialize YOLO model
model = YOLO("C:\\Users\\georg\\Downloads\\yolov8s.pt")

# Set confidence and IoU thresholds
model.overrides['conf'] = 0.70  # Confidence threshold
model.overrides['iou'] = 0.45  # IoU threshold

# Video input and output
video_path = "CodleaBrasov.mp4"
output_path = "output.mp4"

# Open the video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Couldn't open video file.")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_skip = int(fps / 10)  # Process 10 frames per second
print(f"Original FPS: {fps}, Processing every {frame_skip} frames.")

# Define the codec and create VideoWriter object
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video or error reading frame.")
        break

    # Skip frames to process at a fixed frame rate
    if frame_count % frame_skip != 0:
        frame_count += 1
        continue

    frame_count += 1
    print(f"Processing frame {frame_count} with shape: {frame.shape}")

    # Run YOLO detection
    results = model.predict(frame)

    # Annotate frame with detections
    annotated_frame = frame.copy()
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        confidence = box.conf[0]
        class_id = int(box.cls[0])
        label = f"{model.names[class_id]} {confidence:.2f}"

        # Draw the bounding box and label
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the annotated frame and write to output
    cv2.imshow('Pothole Detection', annotated_frame)
    out.write(annotated_frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting on user command.")
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
print("Processing complete. Output saved to:", output_path)

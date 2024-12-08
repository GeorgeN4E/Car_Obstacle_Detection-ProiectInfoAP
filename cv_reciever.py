import cv2
import numpy as np

# Set up the GStreamer pipeline for receiving the stream
gst_pipeline = "udpsrc port=9000 caps='application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264' ! rtph264depay ! avdec_h264 ! videoconvert ! appsink"

# Create a VideoCapture object with the GStreamer pipeline
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to retrieve frame.")
        break

    # Real-time processing example (e.g., grayscale conversion)
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the processed frame
    cv2.imshow("Processed Video", processed_frame)

    # Exit condition (press 'q' to quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture object and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()

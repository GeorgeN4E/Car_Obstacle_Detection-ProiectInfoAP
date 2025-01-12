import cv2

# FFmpeg pipeline for RTP stream
ffmpeg_pipeline = (
    "rtsp://192.168.68.121:9000"  # Example: Replace with your actual stream address
)

cap = cv2.VideoCapture(ffmpeg_pipeline)

if not cap.isOpened():
    print("Error: Unable to open video stream using FFmpeg.")
    exit()

print("Starting video processing...")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to receive frame.")
        break

    # Perform processing on the frame
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the processed frame
    cv2.imshow("Processed Video", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ffmpeg -i udp://192.168.168.110:9000 -f sdl "Stream Output"

import numpy as np
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip

# Region of Interest Selection
def region_selection(image):
    rows, cols = image.shape[:2]
    bottom_left = [cols * 0.2, rows * 0.95]
    top_left = [cols * 0.4, rows * 0.6]
    bottom_right = [cols * 0.8, rows * 0.95]
    top_right = [cols * 0.6, rows * 0.6]
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    mask = np.zeros_like(image)
    ignore_mask_color = 255 if len(image.shape) == 2 else (255,) * image.shape[2]
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    return cv2.bitwise_and(image, mask)

# Hough Transform
def hough_transform(image):
    rho = 1
    theta = np.pi / 180
    threshold = cv2.getTrackbarPos("Hough Threshold", "Adjustments")
    minLineLength = cv2.getTrackbarPos("Min Line Length", "Adjustments")
    maxLineGap = cv2.getTrackbarPos("Max Line Gap", "Adjustments")
    return cv2.HoughLinesP(image, rho, theta, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)

# Line Averaging and Filtering
def average_slope_intercept(lines, image_width):
    left_lines = []
    left_weights = []
    right_lines = []
    right_weights = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - (slope * x1)
            length = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            midpoint = image_width / 2
            if slope < 0 and x1 < midpoint and x2 < midpoint:
                left_lines.append((slope, intercept))
                left_weights.append(length)
            elif slope > 0 and x1 > midpoint and x2 > midpoint:
                right_lines.append((slope, intercept))
                right_weights.append(length)
    left_lane = np.dot(left_weights, left_lines) / np.sum(left_weights) if left_weights else None
    right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if right_weights else None
    return left_lane, right_lane

# Convert Slope/Intercept to Points
def pixel_points(y1, y2, line):
    if line is None:
        return None
    slope, intercept = line
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, int(y1)), (x2, int(y2))

# Draw Lane Lines
def draw_lane_lines(image, lines):
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            pt1, pt2 = line
            cv2.line(line_image, pt1, pt2, (255, 0, 0), 12)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

# Adjustments for Debugging
def adjust_parameters():
	#Try to close the "Adjustments" window if it exists
    try:
        cv2.destroyWindow("Adjustments")
    except cv2.error:
        pass  # Ignore if the window doesn't exist
    # Create a new adjustments window with specified size
    cv2.namedWindow("Adjustments", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Adjustments", 400, 300)  # Set slider window size
    cv2.createTrackbar("Low Threshold", "Adjustments", 50, 600, lambda x: None)
    cv2.createTrackbar("High Threshold", "Adjustments", 150, 600, lambda x: None)
    cv2.createTrackbar("Hough Threshold", "Adjustments", 20, 100, lambda x: None)
    cv2.createTrackbar("Min Line Length", "Adjustments", 20, 100, lambda x: None)
    cv2.createTrackbar("Max Line Gap", "Adjustments", 50, 200, lambda x: None)
    cv2.createTrackbar("Exclude Left", "Adjustments", 0, 50, lambda x: None)  # Left exclusion (0-50%)
    cv2.createTrackbar("Exclude Right", "Adjustments", 0, 50, lambda x: None)  # Right exclusion (0-50%)



	# Canny edge detection thresholds
    low_threshold = 447
    high_threshold = 151

    # Hough transform parameters
    rho = 1
    theta = np.pi / 180
    hough_threshold = 5
    min_line_length = 13
    max_line_gap = 0
    exclude_left = 32
    exclude_right = 25

    # Explicitly set the default values
    cv2.setTrackbarPos("Low Threshold", "Adjustments", low_threshold)
    cv2.setTrackbarPos("High Threshold", "Adjustments", high_threshold)
    cv2.setTrackbarPos("Hough Threshold", "Adjustments", hough_threshold)
    cv2.setTrackbarPos("Min Line Length", "Adjustments", min_line_length)
    cv2.setTrackbarPos("Max Line Gap", "Adjustments", max_line_gap)
    cv2.setTrackbarPos("Exclude Left", "Adjustments", exclude_left)  # Left exclusion (0-50%)
    cv2.setTrackbarPos("Exclude Right", "Adjustments", exclude_right)  # Right exclusion (0-50%)


# Frame Processing
def frame_processor(image):
    adjust_parameters()  # Initialize sliders

    while True:
        # Get current slider positions
        low_t = cv2.getTrackbarPos("Low Threshold", "Adjustments")
        high_t = cv2.getTrackbarPos("High Threshold", "Adjustments")
        exclude_left_percent = cv2.getTrackbarPos("Exclude Left", "Adjustments")  # Left exclusion
        exclude_right_percent = cv2.getTrackbarPos("Exclude Right", "Adjustments")  # Right exclusion

        # Convert percentage to pixel values
        exclude_left_x = int(image.shape[1] * exclude_left_percent / 100)
        exclude_right_x = int(image.shape[1] * (1 - exclude_right_percent / 100))

        # Process frame
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
        edges = cv2.Canny(blur, low_t, high_t)

        # Exclude the parts of the screen on the left and right
        edges[:, :exclude_left_x] = 0  # Mask the left region
        edges[:, exclude_right_x:] = 0  # Mask the right region

        # Visualize the exclusion lines
        image_with_lines = image.copy()
        cv2.line(image_with_lines, (exclude_left_x, 0), (exclude_left_x, image.shape[0]), (0, 255, 0), 2)  # Left line
        cv2.line(image_with_lines, (exclude_right_x, 0), (exclude_right_x, image.shape[0]), (255, 0, 0), 2)  # Right line

        # Region selection and Hough Transform
        region = region_selection(edges)
        lines = hough_transform(region)

        # Process detected lines
        if lines is not None:
            left_lane, right_lane = average_slope_intercept(lines, image.shape[1])
            lane_lines_points = [
                pixel_points(image.shape[0], image.shape[0] * 0.6, left_lane),
                pixel_points(image.shape[0], image.shape[0] * 0.6, right_lane)
            ]
            result = draw_lane_lines(image_with_lines, lane_lines_points)
        else:
            result = image_with_lines

        # Resize and display windows
        cv2.namedWindow("Edges", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Edges", 640, 480)  # Set window size
        cv2.imshow("Edges", edges)

        cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Result", 800, 600)  # Set window size
        cv2.imshow("Result", result)

        # Exit loop on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return result

# Process Video
def process_video_opencv(input_path, output_path):
	# Dynamically create a descriptive filename

    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = frame_processor(frame)
        out.write(processed_frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Call the Function
process_video_opencv('input.mp4', 'output.mp4')

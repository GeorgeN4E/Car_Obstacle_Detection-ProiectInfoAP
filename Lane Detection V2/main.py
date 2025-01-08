import cv2
import numpy as np

def region_selection(image):
    """
    Define a region of interest for lane detection.
    """
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

def hough_transform(image, rho, theta, threshold, min_line_length, max_line_gap):
    """
    Perform Hough Transform to detect lines.
    """
    return cv2.HoughLinesP(image, rho, theta, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)

def average_slope_intercept(lines, image_width):
    """
    Compute averaged slope and intercept for left and right lanes.
    """
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

def pixel_points(y1, y2, line):
    """
    Convert line slope and intercept to pixel points.
    """
    if line is None:
        return None
    slope, intercept = line
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return (x1, int(y1)), (x2, int(y2))

def draw_lane_lines(image, lines):
    """
    Draw lane lines on the image.
    """
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            pt1, pt2 = line
            cv2.line(line_image, pt1, pt2, (255, 0, 0), 12)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

def process_frame(frame, low_t, high_t, rho, theta, threshold, min_line_length, max_line_gap):
    """
    Process a single frame with the given parameters.
    """
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grayscale, (5, 5), 0)
    edges = cv2.Canny(blur, low_t, high_t)
    region = region_selection(edges)
    lines = hough_transform(region, rho, theta, threshold, min_line_length, max_line_gap)
    if lines is not None:
        left_lane, right_lane = average_slope_intercept(lines, frame.shape[1])
        lane_lines_points = [
            pixel_points(frame.shape[0], frame.shape[0] * 0.6, left_lane),
            pixel_points(frame.shape[0], frame.shape[0] * 0.6, right_lane)
        ]
        result = draw_lane_lines(frame, lane_lines_points)
    else:
        result = frame
    return result

def process_video(input_path, output_path, low_t, high_t, hough_params):
    """
    Process the entire video using specified parameters.
    """
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
        processed_frame = process_frame(frame, low_t, high_t, *hough_params)
        out.write(processed_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Input parameters
    input_video = "input.mp4"
    output_video = "output.mp4"

    """Default Params    
    # Canny edge detection thresholds
    low_threshold = 50
    high_threshold = 150

    # Hough transform parameters
    rho = 1
    theta = np.pi / 180
    hough_threshold = 20
    min_line_length = 40
    max_line_gap = 150
    """

    # Canny edge detection thresholds
    low_threshold = 230
    high_threshold = 415

    # Hough transform parameters
    rho = 1
    theta = np.pi / 180
    hough_threshold = 15
    min_line_length = 50
    max_line_gap = 200


    # Process video
    hough_params = (rho, theta, hough_threshold, min_line_length, max_line_gap)
    process_video(input_video, output_video, low_threshold, high_threshold, hough_params)

import cv2
video = cv2.VideoCapture('rtspsrc location=<<rtsp URL>> latency=0 ! queue ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
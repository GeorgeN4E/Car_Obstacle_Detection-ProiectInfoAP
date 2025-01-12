#!/usr/bin/python3
from time import sleep
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for video streaming
picam2.configure(picam2.create_video_configuration(main={"size": (1280, 720),
                                                         "format": "YUV420"}))

# Start the recording and stream via UDP to the specified IP and port
picam2.start_recording(H264Encoder(), output=FfmpegOutput("-f rawvideo -pix_fmt yuv420p udp://192.168.137.1:9000"))
#picam2.start_recording(H264Encoder(), output=FfmpegOutput("-f rtp udp://192.168.137.1:9000"))

count = 0
while True:
    print(f'streaming... [{count}]')
    count += 1
    sleep(2)
import socket
import struct
import pickle
import time
from picamera2 import Picamera2
import numpy as np

def debug_camera(server_ip, server_port):
    # Step 1: Check Camera
    print("Testing camera...")
    try:
        # Initialize picamera2
        picam2 = Picamera2()
        picam2.start()

        print("Camera is working and capturing frames.")

        # Step 2: Test Data Transmission
        print("Testing data transmission...")
        try:
            # Create a socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((server_ip, server_port))
            server_socket.listen(1)
            print(f"Waiting for a connection on {server_ip}:{server_port}...")
            conn, addr = server_socket.accept()
            print(f"Connection established with {addr}")

            for i in range(10):  # Send 10 frames for testing
                # Capture a frame
                frame = picam2.capture_array()  # Capture the frame as a numpy array

                # Serialize the frame
                data = pickle.dumps(frame)
                message_size = struct.pack("Q", len(data))

                # Send the frame
                conn.sendall(message_size + data)
                print(f"Frame {i + 1} sent (size: {len(data)} bytes).")

            print("Data transmission test completed.")
        except Exception as e:
            print(f"Error during transmission: {e}")
        finally:
            server_socket.close()
            print("Server socket closed.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        picam2.close()
        print("Camera resources released.")

if __name__ == "__main__":
    SERVER_IP = "192.168.137.236"  # Replace with your Raspberry Pi's IP address
    SERVER_PORT = 9999
    debug_camera(SERVER_IP, SERVER_PORT)

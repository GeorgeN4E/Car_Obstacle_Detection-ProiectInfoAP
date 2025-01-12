import socket
import struct
import pickle
import os

def receive_images(server_ip, server_port, save_folder):
    # Step 1: Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"Created folder '{save_folder}' to save received images.")
    
    print("Waiting for images from the Raspberry Pi...")

    try:
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        while True:
            # Step 2: Receive the message size (8 bytes)
            packed_msg_size = client_socket.recv(8)
            if not packed_msg_size:
                print("Connection closed by the sender.")
                break
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            # Step 3: Receive the full image data
            data = b""
            while len(data) < msg_size:
                packet = client_socket.recv(4096)
                if not packet:
                    break
                data += packet
            
            # Step 4: Deserialize the image data
            image_data = pickle.loads(data)

            # Step 5: Save the image to the folder
            image_filename = os.path.join(save_folder, f"image_{len(os.listdir(save_folder)) + 1}.jpg")
            with open(image_filename, "wb") as f:
                f.write(image_data)
            print(f"Received and saved image as '{image_filename}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Client socket closed.")

if __name__ == "__main__":
    SERVER_IP = "192.168.137.236"  # Replace with your Raspberry Pi's IP address
    SERVER_PORT = 9999
    SAVE_FOLDER = "./received_images"  # Folder to save the received images
    receive_images(SERVER_IP, SERVER_PORT, SAVE_FOLDER)

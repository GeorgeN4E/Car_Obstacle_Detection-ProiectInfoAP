
import socket
import struct
import pickle
import cv2  # For displaying received frames


def receive_frames(server_ip, server_port):
    print(f"Connecting to {server_ip}:{server_port}...")
    
    try:
        # Create a socket and connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))
        print("Connection established!")
        
        data = b""
        payload_size = struct.calcsize("Q")  # Size of the header indicating frame size
        
        while True:
            # Receive the frame size first
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # Receive data in chunks
                if not packet:
                    print("No more data from server. Exiting...")
                    return
                data += packet
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            
            # Receive the entire frame based on the size
            while len(data) < msg_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    print("Incomplete data received. Exiting...")
                    return
                data += packet
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Deserialize the frame
            frame = pickle.loads(frame_data)
            print(f"Received a frame of shape {frame.shape}.")
            
            # Display the frame (optional)
            cv2.imshow("Received Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        client_socket.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    SERVER_IP = "192.168.137.236"  # Replace with your Raspberry Pi's IP
    SERVER_PORT = 9999
    receive_frames(SERVER_IP, SERVER_PORT)

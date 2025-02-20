import socket
import json

# Server configuration
HOST = "127.0.0.1"  # Change this if running on a remote server
PORT = 9999         # Must match the port your server is running on

def start_client():
    """Connects to the server and receives the finance price stream."""
    
    # Create a TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the finance server
        client.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        # Continuously receive data from the server
        while True:
            data = client.recv(1024).decode("utf-8")  # Receive data in chunks of 1024 bytes
            
            if not data:
                print("Server closed connection.")
                break  # Exit if the server closes connection

            try:
                # Parse JSON message received from the server
                message = json.loads(data.strip())
                
                # Print or process the finance data
                print(f"Received Finance Data: {message}")

            except json.JSONDecodeError:
                print("Error: Received invalid JSON data.")

    except ConnectionRefusedError:
        print("Error: Could not connect to server. Make sure it is running.")
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        client.close()  # Ensure socket is closed when done

# Run the client
if __name__ == "__main__":
    start_client()
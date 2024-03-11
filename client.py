import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.239.219', 12345)  # Use the actual local IP address of your server
    timeout = 10  # Increase the timeout to 10 seconds

    client_socket.settimeout(timeout)  # Set socket timeout
    try:
        # Attempt to connect to the server
        client_socket.connect(server_address)
        # Receive the message from the server
        data = client_socket.recv(1024)
        print('Received from server:', data.decode())

    except socket.timeout:
        print("Connection attempt timed out. Check server availability and network settings.")

    except Exception as e:
        print("Error:", e)

    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
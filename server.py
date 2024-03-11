import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)

    server_socket.bind(server_address)
    server_socket.listen(1)

    print('Server listening on {}:{}'.format(*server_address))

    while True:
        connection, client_address = server_socket.accept()
        try:
            print('Connection from', client_address)

            # Send a message to the client
            message_to_client = "Bhavika wants to join you ride!"
            connection.sendall(message_to_client.encode())

        finally:
            connection.close()

if __name__ == "__main__":
    start_server()

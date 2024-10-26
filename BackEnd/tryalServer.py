import socket
def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Server listening on {host}:{port}')

    conn, addr = server_socket.accept()
    print(f'Connection from {addr}')

    with open('received_image.jpg', 'wb') as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)

    print('Image received successfully.')
    conn.close()
    server_socket.close()

if __name__ == '__main__':
    start_server()
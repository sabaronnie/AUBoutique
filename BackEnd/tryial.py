import socket

def send_image(image_path, host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    with open(image_path, 'rb') as f:
        data = f.read(4096)
        while data:
            client_socket.send(data)
            data = f.read(4096)

    print('Image sent successfully.')
    client_socket.close()

if __name__ == '__main__':
    send_image('path_to_your_image.jpg')

import socket
import traceback

HOST = "localhost" # replace this with your pc's ip address
PORT = 65432 # match this with `PORT` in `receiver.py`
TIMEOUT = 4

def clean(client_socket):
    if client_socket is not None:
        client_socket.close()

def send_request(request):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        print(f"attempting connection with server {(HOST, PORT)}")
        client_socket.connect((HOST, PORT))
        print(f"connection successful, sending request '{request}'")
        client_socket.sendall(request.encode())
        data = client_socket.recv(1024)
        clean(client_socket)
        return data
    except ConnectionRefusedError:
        print("connection with server failed")
        return None
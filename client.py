import socket
import traceback

HOST = "localhost" # replace this with your pc's ip address
PORT = 65432 # match this with `PORT` in `receiver.py`
TIMEOUT = 4

def clean(client_socket):
    if client_socket is not None:
        client_socket.close()
        print("closing client socket...")

def send_request():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)
    print(f"attempting connection with server {(HOST, PORT)}")
    client_socket.connect((HOST, PORT))
    print("connection successful, sending monitor input switch request...")
    client_socket.sendall(b"switch")
    data = client_socket.recv(1024)
    if data == b"switch":
        print(f"success! received {data!r} back from server")
        clean()
        return True
    else:
        print("input switch request failed")
        clean()
        return False
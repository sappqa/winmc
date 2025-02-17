import socket
import traceback
from config import *

def clean(client_socket):
    if client_socket is not None:
        client_socket.close()

def send_request(request, suppress=False):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        if not suppress: print(f"attempting connection with server {(HOST, PORT)}")
        client_socket.connect((HOST, PORT))
        if not suppress: print(f"connection successful, sending request '{request}'")
        client_socket.sendall(request.encode())
        data = client_socket.recv(1024)
        clean(client_socket)
        return data
    except ConnectionRefusedError:
        if not suppress: print("connection with server failed")
        return None
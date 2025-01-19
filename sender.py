import socket
import traceback

HOST = "localhost" # replace this with your pc's ip address
PORT = 65432 # match this with `PORT` in `receiver.py`
TIMEOUT = 4

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)
    print(f"attempting connection with {(HOST, PORT)}")
    client_socket.connect((HOST, PORT))
    print("connection successful, sending monitor input switch request...")
    client_socket.sendall(b"switch")
    data = client_socket.recv(1024)
    print(f"success! received {data!r} back from server")
except Exception:
    traceback.print_exc()
finally:
    client_socket.close()
    print("exiting...")
import socket
import select
import threading
import traceback
import signal

HOST = "localhost" # replace this with your pc's ip address. you can get this using the `ipconfig` command
PORT = 65432 # this is the port you will open for listening on your pc. use any port in the dynamic port range 49152 to 65535
TIMEOUT = 4.0
interrupt_receive, interrupt_send = socket.socketpair()
interrupt_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
interrupt_send.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def server_thread():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_watchlist = [server_socket, interrupt_receive]
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        server_socket.setblocking(False)
        print("server is up and running!")
        
        active = True
        client = None
        while active:
            print("waiting on monitor input switch request from client... use 'ctrl+c' to cancel")
            readable, writable, error = select.select(socket_watchlist, [], [])
            for s in readable:
                if s is interrupt_receive:
                    print("exit interrupt received")
                    active = False
                    break
                if s is server_socket:
                    client_socket, client_address = server_socket.accept()
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    client = client_socket
                    print(f"accepted connection from client! {client_address}")
                    client_socket.setblocking(False)
                    socket_watchlist.append(client_socket)
                else:
                    if isinstance(s, socket.socket):
                        data = s.recv(1024)
                        if data:
                            print(f"received data: {data!r} from client {s.getsockname()}\n")
                            s.sendall(data)
                        else:
                            print(f"client disconnected")
                            client_socket.close()
                            client = None
                            socket_watchlist.remove(client_socket)
    except Exception:
        traceback.print_exc()
    finally:
        server_socket.close()
        interrupt_receive.close()
        interrupt_send.close()
        if client is not None:
            client.close()

def handle_sigint(signum, frame):
    raise KeyboardInterrupt

try:
    signal.signal(signal.SIGINT, handle_sigint)
    server = threading.Thread(target=server_thread, daemon=False)
    server.start()
    while server.is_alive():
        server.join(timeout=0.5)
except KeyboardInterrupt:
    print("sending interrupt to the server...")
    interrupt_send.send(b"\x01")
    server.join()
    print("exiting...")
except Exception:
    traceback.print_exc()


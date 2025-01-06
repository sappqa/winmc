import socket

HOST = "your_pc's_ip_address" # you can get this using the `ipconfig` command
PORT = 65432 # use any port in the dynamic port range 49152 to 65535
TIMEOUT = 8.0

# may want to use a non-blocking socket if possible
# need to write interrupt mechanism, ex: esc or some other keyboard input to stop the program.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(TIMEOUT)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # blocking
    with conn:
        print(f"connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

print("done")
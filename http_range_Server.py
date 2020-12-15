import threading
import socket
import argparse
import sys, os


def multi_threaded_client(conn):
    while True:
        data = conn.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        conn.sendall(str.encode(response))
    conn.close()

def main():
    # Set up argument parsing automation
    prog = 'python3 http_range_server.py'
    descr = 'HTTP Server that accepts range requests'
    parser = argparse.ArgumentParser(prog=prog, description=descr)
    parser.add_argument('-w', '--objects_dir', type=str, default=None, required=True, help='Directory of objects')
    parser.add_argument('-p', '--server_port', type=int, default=None, required=True, help='Port')

    args = parser.parse_args()

    port = args.server_port
    thread_count = 0

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server_socket.bind(('',port))
    except socket.error as e:
        print(str(e))

    server_socket.listen(1)

    while True:
        client, address = server_socket.accept()
        threading.


if __name__ == '__main__':
    main()
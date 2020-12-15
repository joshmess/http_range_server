import _thread
import socket
import argparse
import sys, os
import time


def client_thread(conn,objects):
    while True:
        data = conn.recv(2048)
        request = data.decode()
        space = request.find(" ")
        type = request[0:space]
        

        
        # Lookup requested object
        for obj in objects:
            if type == "GET" and str(obj) in request:
                response = obj.encode()
            if type == "HEAD" and str(obj) in request:
                time = time.time()
                response = 'Time %s\nServer: CSCI 6760 Final\nSize: %d' % (time, len(obj))

        conn.sendall(response)
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
    dir_path = args.objects_dir

    # test using directory
    if dir_path:
        obj_list = []

        for folder, subfolder, files in os.walk(dir_path):
            for f in files:
                complete_path = os.path.join(folder, f)
                obj_list.append(complete_path)

        threads = 0

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind(('', port))
        except socket.error as e:
            print(str(e))

        print('Server is listening...')
        server_socket.listen(1)

        while True:
            client, address = server_socket.accept()
            msg = 'Connected to: ' + address[0] + ':' + str(address[1])
            print(msg)
            _thread.start_new_thread(client_thread(client, obj_list))
            threads += 1


if __name__ == '__main__':
    main()

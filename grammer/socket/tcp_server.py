import socket
from _thread import *

HOST_IP = "127.0.0.1"
PORT = 9000
BUFSIZE = 512
client_sockets = []


def tcp_server_init() -> None:
    print(">> Server Start with ip : {}".format(HOST_IP))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST_IP, PORT))
    server_socket.listen(socket.SOMAXCONN)

    try:
        while True:
            print(">> Wait")

            client_socket, addr = server_socket.accept()
            client_sockets.append(client_socket)
            start_new_thread(process_client, (client_socket, addr))
            print("참가자 수 : {}".format(len(client_sockets)))

    except Exception as e:
        print("에러: {}".format(e))

    finally:
        server_socket.close()


def process_client(client_socket, addr) -> None:
    print(">> Connected by : {}:{}".format(addr[0], addr[1]))

    while True:
        try:
            data = client_socket.recv(BUFSIZE)

            if not data:
                print(">> Disconnected by {}:{}".format(addr[0], addr[1]))
                break

            print(">> Received from {}:{} = {}".format(addr[0], addr[1], data.decode()))

            for client in client_sockets:
                if client != client_socket:
                    client.send(data)

        except ConnectionResetError as e:
            print(">> Disconnected by {}:{} = {}".format(addr[0], addr[1], e.__traceback__))
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print("remove client list: {}".format(len(client_sockets)))

    client_socket.close()


if __name__ == "__main__":
    tcp_server_init()
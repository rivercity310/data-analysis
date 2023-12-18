import socket
from _thread import *
from tcp_server import HOST_IP, PORT, BUFSIZE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
client_socket.connect((HOST_IP, PORT))


def recv_data(client_socket):
    while True:
        data = client_socket.recv(BUFSIZE)
        print("receive: {}".format(repr(data.decode())))


start_new_thread(recv_data, (client_socket,))
print(">> Connect Server")

while True:
    message = input()
    if message == 'quit':
        close_data = message
        break

    client_socket.send(message.encode())

client_socket.close()

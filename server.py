import socket
import time
import select

HEADER_SIZE = 10
IP = socket.gethostname()
PORT = 1234
ENCODE_STAND = 'utf-8'


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_SIZE)
        if not len(message_header):
            return False

        message_length = int(message_header.decode(ENCODE_STAND).strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((IP, PORT))
    server_socket.listen(5)

    sockets_list = [server_socket]

    clients = {}

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()

                user = receive_message(client_socket)

                if user is False:
                    continue

                sockets_list.append(client_socket)
                clients[client_socket] = user

                print(
                    f'accepted new connection from {client_address[0]}:{client_address[1]} '
                    f'username:{user["data"].decode(ENCODE_STAND)}')
            else:
                message = receive_message(notified_socket)
                if message is False:
                    print(f'Colsed connection from {clients[notified_socket]["data"].decode(ENCODE_STAND)}')
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    continue

                user = clients[notified_socket]
                print(f'Received message from {user["data"].decode(ENCODE_STAND)}: {message["data"].decode(ENCODE_STAND)}')
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]

        # client_socket, address = server_socket.accept()
        # print(f'Connection from {address} has been established!')
        #
        # msg = 'Welcome to the server!'
        # msg = f'{len(msg):<{HEADER_SIZE}}' + msg
        #
        # client_socket.send(bytes(msg, ENCODE_STAND))
        #
        # while True:
        #     time.sleep(3)
        #     msg = f'The time is {time.time()}'
        #     msg = f'{len(msg):<{HEADER_SIZE}}' + msg
        #     client_socket.send(bytes(msg, ENCODE_STAND))


if __name__ == '__main__':
    main()

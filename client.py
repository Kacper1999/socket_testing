import socket
import select
import errno
import sys
from server import HEADER_SIZE, IP, PORT, ENCODE_STAND


def main():
    my_username = input('Username: ')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    username = my_username.encode(ENCODE_STAND)
    username_header = f'{len(username):<{HEADER_SIZE}}'.encode(ENCODE_STAND)
    client_socket.send(username_header + username)

    while True:
        message = input(f'{my_username} > ')
        if message:
            message = message.encode(ENCODE_STAND)
            message_header = f'{len(message) :< {HEADER_SIZE}}'.encode(ENCODE_STAND)
            client_socket.send(message_header + message)

        try:
            while True:
                # receive things
                username_header = client_socket.recv(HEADER_SIZE)
                if not len(username_header):
                    print('connection closed by the server')
                    sys.exit()
                username_length = int(username_header.decode(ENCODE_STAND).strip())  # maybe wrong
                username = client_socket.recv(username_length).decode(ENCODE_STAND)

                message_header = client_socket.recv(HEADER_SIZE)
                message_length = int(message_header.decode(ENCODE_STAND).strip())
                message = client_socket.recv(message_length).decode(ENCODE_STAND)

                print(f'{username} > {message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('reading error', str(e))
                sys.exit()
            continue
        except Exception as e:
            print('General error', str(e))


        # full_msg = ''
        # new_msg = True
        # while True:
        #     msg = client_socket.recv(16)
        #     if new_msg:
        #         print(f'new message length: {msg[:HEADER_SIZE]}')
        #         msg_len = int(msg[:HEADER_SIZE])
        #         new_msg = False
        #
        #     full_msg += msg.decode('utf-8')
        #
        #     if len(full_msg) - HEADER_SIZE == msg_len:
        #         print('full msg received')
        #         print(full_msg[HEADER_SIZE:])
        #         new_msg = True
        #         full_msg = ''
        #
        # print(full_msg)
        #


if __name__ == '__main__':
    main()

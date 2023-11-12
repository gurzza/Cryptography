import socket
import os
import threading
import hashlib
from Crypto.Random import get_random_bytes

import myIDEA
import myRSA

# Create Socket (TCP) Connection
ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
HOSTNAME = socket.gethostname()
HOST_IP = socket.gethostbyname(HOSTNAME)
PORT = 8081
ThreadCount = 0
MAX_CONNECTIONS = 5
N_KEYS = [None] * MAX_CONNECTIONS
E_KEYS = [None] * MAX_CONNECTIONS
FreeID = [i for i in range(MAX_CONNECTIONS)]

try:
    ServerSocket.bind((HOST_IP, PORT))
except socket.error as e:
    print(str(e))

print('Waiting for a Connection..')
ServerSocket.listen(5)


# HashTable = {}


def get_filename(connection):
    fileFlag = False

    while not fileFlag:
        connection.send('Enter the name of file that you want to get'.encode())
        filename = connection.recv(1024).decode()
        # print(filename)
        fileFlag = os.path.isfile(filename)  # True if exist
        connection.send(str(fileFlag).encode())

    return filename


# Function : For each client


def xor_bytes(a, b):
    a = str(a).encode()
    b = str(b).encode()
    res = bytes(i ^ j for i, j in zip(a, b))
    return int.from_bytes(res, 'big')


def encrypt_text(key, plain, iv):
    my_IDEA = myIDEA.IDEA(key)
    #print('PLAIN: ', plain)
    plain = int.from_bytes(plain.encode("ASCII"), 'big')
    size = plain.bit_length()

    #print('BEFORE ENC:\n', plain)
    sub_plain = []
    sub_enc = []
    sub_plain_c = []
    sub_enc_c = []
    # Encryption
    x = size // 64
    if size % 64 != 0:
        x += 1
        size += 64 - size % 64
    #print('size, x:', size, x)

    prev_cipher = iv
    for i in range(x):
        shift = size - (i + 1) * 64
        #print('shift: ', shift)
        sub_plain.append((plain >> shift) & 0xFFFFFFFFFFFFFFFF)
        sub_plain_c.append((plain >> shift) & 0xFFFFFFFFFFFFFFFF)

        #encrypted = xor_bytes(sub_plain[i], my_IDEA.encrypt(prev_cipher))
        encrypted = sub_plain[i] ^ my_IDEA.encrypt(int(prev_cipher))
        encrypted_c = my_IDEA.encrypt(sub_plain[i])

        #print(sub_plain[i], ' ', my_IDEA.encrypt(int(prev_cipher)), ' ', encrypted)


        sub_enc.append(encrypted)
        sub_enc_c.append(encrypted_c)
        # encrypted = 0
        prev_cipher = encrypted
        #print(prev_cipher, '\n')
    encrypted = 0
    encrypted_c = 0
    for i in range(x):
        sub_enc[i] = sub_enc[i] << (x - (i + 1)) * 64
        sub_enc_c[i] = sub_enc_c[i] << (x - (i + 1)) * 64

        encrypted = encrypted | sub_enc[i]
        encrypted_c = encrypted_c | sub_enc_c[i]


    #print('typetype: ', type(encrypted))
    #print('check_c:\n', encrypted)
    return encrypted
    #return hex(encrypted)


def encrypt_file(sc, filename, conID):
    session_key = int(get_random_bytes(16).hex(), 16)
    # print('SERVER SESSION KEY: ', int(session_key, 16))
    enc_session_key = myRSA.MessageEnc(session_key, N_KEYS[conID], E_KEYS[conID])
    sc.send(str(enc_session_key).encode())
    with open(filename, 'r') as f:
        text = f.read()
        iv = get_random_bytes(8)
        iv = int.from_bytes(iv, byteorder='little')
        #print('iv: ', type(iv))
        enc_text = encrypt_text(session_key, text, iv)
        # print(enc_text)
        sc.send(str(enc_text).encode())
        #print(enc_text)
        trash = sc.recv(1024).decode()
        sc.send(str(iv).encode())
        # !!!!!!!!!!!!!!!!!!!!


def threaded_client(connection, connectionID):
    print('ID: ' + str(connectionID))

    client_data = connection.recv(1024).decode()
    while client_data.upper() != 'QUIT' and client_data.upper() != 'Q':

        if client_data.upper() == 'FILE' or client_data.upper() == 'F':
            filename = get_filename(connection)
            # session key
            session_key = get_random_bytes(16)  # bytes = 128 bits
            # connection.send(str(session_key).encode())
            encrypt_file(connection, filename, connectionID)

        elif client_data.upper() == 'GENERATE KEY' or client_data.upper() == 'GK':
            n = int(connection.recv(2048).decode())
            e = int(connection.recv(2048).decode())
            N_KEYS[connectionID] = int(n)
            E_KEYS[connectionID] = int(e)
            # print(str(n) + '\n' + str(e))
        client_data = connection.recv(2048).decode()

    ##########
    # print(f"Closing the socket with client {current_socket.getpeername()} now...")
    print('GO HOME!')
    global ThreadCount
    N_KEYS[connectionID] = None
    E_KEYS[connectionID] = None
    FreeID.append(connectionID)
    connection.close()
    ThreadCount -= 1
    """the whole disconnection sequence is triggered from the exception handler, se we will just raise the exception
        to close the server socket"""


while True:
    Client, address = ServerSocket.accept()
    connectionID = FreeID.pop(0)
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client, connectionID)
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
    if ThreadCount == 0:
        break
ServerSocket.close()

# # server side:
#
# import socket
# import select
# import time
# import random
# import cryptography.hazmat.primitives.ciphers
# import os
#
# MAX_CONNECTION = 5
# HOSTNAME = socket.gethostname()
# HOST_IP = socket.gethostbyname(HOSTNAME)
# PORT = 5050
# ADDR = (HOST_IP, PORT)
# freeID = [i for i in range(MAX_CONNECTION)]
# N_KEY = [None] * MAX_CONNECTION
# E_KEY = [None] * MAX_CONNECTION
#
#
# def all_sockets_closed(server_socket, starttime):
#     """closes the server socket and displays the duration of the connection"""
#     print("\n\nAll Clients Disconnected\nClosing The Server...")
#     endtime = time.time()
#     elapsed = time.strftime("%H:%M:%S", time.gmtime(endtime - starttime))
#     unit = (
#         "Seconds"
#         if elapsed < "00:01:00"
#         else "Minutes"
#         if "01:00:00" > elapsed >= "00:01:00"
#         else "Hours"
#     )
#     server_socket.close()
#     print(f"\nThe Server Was Active For {elapsed} {unit}\n\n")
#
#
# def active_client_sockets(connected_sockets):
#     """prints the IP and PORT of all connected sockets"""
#     print("\nCurrently Connected Sockets:")
#     for c in connected_sockets:
#         print("\t", c.getpeername())  # ('IP', PORT)
#
#
# # args by order: current socket being served, server socket, all sockets being connected, start time
# def get_filename(current_socket):
#     fileFlag = False
#
#     while not fileFlag:
#         current_socket.send('Enter the name of file that you want to get'.encode())
#         filename = current_socket.recv(1024).decode()
#         # print(filename)
#         fileFlag = os.path.isfile(filename)  # True if exist
#         if not fileFlag:
#             current_socket.send(str(fileFlag).encode())
#     return filename
#
#
# def serve_client(current_socket, connectionID, server_socket, connected_sockets, starttime):
#     #current_socket.send(str(current_socket).encode())
#     """Takes the msg received from the client and handles it accordingly"""
#     try:
#         client_data = current_socket.recv(1024).decode()
#         date_time = time.strftime("%d/%m/%Y, %H:%M:%S")
#         print(f"\nReceived new message form client {current_socket.getpeername()} at {date_time}:")
#
#
#     except ConnectionResetError:
#         print(f"\nThe client {current_socket.getpeername()} has disconnected...")
#         connected_sockets.remove(current_socket)
#         current_socket.close()
#         if len(connected_sockets) != 0:  # check for other connected sockets
#             active_client_sockets(connected_sockets)
#         else:
#             raise ValueError
#         """the whole disconnection sequence is triggered from the exception handler, se we will just raise the exception
#                 to close the server socket"""
#     else:
#         print('OPERATION: client_data\n', 'ID: ' + str(connectionID))
#         if client_data.upper() == 'FILE' or client_data.upper() == 'F':
#             filename = get_filename(current_socket)
#             # print(filename)
#         elif client_data.upper() == 'GENERATE KEY' or client_data.upper() == 'GK':
#             n = int(current_socket.recv(2048).decode())
#             e = int(current_socket.recv(1024).decode())
#             N_KEY[connectionID] = n
#             E_KEY[connectionID] = e
#
#
#
#
#         elif client_data.upper() == 'QUIT' or client_data.upper() == 'Q':  # close connection with the client and close socket
#             print(f"Closing the socket with client {current_socket.getpeername()} now...")
#             current_socket.send("Bye".encode())
#             # tell the client we accepted his request to disconnect, also disconnect the client from their side
#             connected_sockets.remove(current_socket)
#             N_KEY[connectionID] = None
#             E_KEY[connectionID] = None
#             freeID.append(connectionID)
#
#             current_socket.close()
#             if len(connected_sockets) != 0:
#                 active_client_sockets(connected_sockets)
#             else:
#                 raise ValueError
#             """the whole disconnection sequence is triggered from the exception handler, se we will just raise the exception
#                 to close the server socket"""
#
#         else:
#             current_socket.send(client_data.encode())
#             print("Responded by: Sending the message back to the client")
#
#
# def main():
#     """server setup and socket handling"""
#     print("Setting up server...")
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(ADDR)
#
#     server_socket.listen(MAX_CONNECTION)
#     print("\n* Server is ON *\n")
#     print("Waiting for clients to establish connection...")
#     starttime = time.time()
#     connected_sockets = []  # list of the client sockets being connected
#     try:
#         while True:
#             ready_to_read, ready_to_write, in_error = select.select(
#                 [server_socket] + connected_sockets, [], []
#             )
#             for current_socket in ready_to_read:
#                 if current_socket is server_socket:  # if the current socket is the new socket we receive from the server
#                     (client_socket, client_address) = current_socket.accept()
#                     print("\nNew client joined!", client_address)
#                     connected_sockets.append(client_socket)
#                     active_client_sockets(connected_sockets)
#                     continue
#
#                 connectionID = freeID.pop(0)
#                 serve_client(current_socket, connectionID, server_socket, connected_sockets, starttime)
#
#     except ValueError:
#         # occurs when the last client connected is forcibly closing the socket (and not by Sending 'q' or 'quit'),
#         # and the server keeps scanning with the 'select()' method.
#         # In this case the select method will return -1 and raise an exception for value error.
#         # we know that this exception can be raised only when the list of connected sockets is empty, so we will call a function to close the server socket.
#
#         all_sockets_closed(server_socket, starttime)
#         pass
#
#
# if __name__ == "__main__":
#     main()

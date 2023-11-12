import socket
import socket
import sys
from Crypto.PublicKey import RSA

import myIDEA
import myRSA

SERVER_NAME = 'DESKTOP-7FRD9J8'
SERVER_IP = socket.gethostbyname(SERVER_NAME)
PORT = 8081
N_KEY = None
E_KEY = None
P_KEY = None
Q_KEY = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


def xor_bytes(a, b):
    a = str(a).encode()
    b = str(b).encode()
    res = bytes(i ^ j for i, j in zip(a, b))
    return int.from_bytes(res, 'big')


def decrypt_text(key, cipher, iv):
    my_IDEA = myIDEA.IDEA(key)
    #plain = int.from_bytes(plain.encode("ASCII"), 'big')
    #!!!!!!!
    cipher = int(cipher)
    iv = int(iv)

    size = cipher.bit_length()

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
        sub_plain.append((cipher >> shift) & 0xFFFFFFFFFFFFFFFF)
        sub_plain_c.append((cipher >> shift) & 0xFFFFFFFFFFFFFFFF)


        # encrypted = xor_bytes(sub_plain[i], my_IDEA.encrypt(prev_cipher))
        encrypted = int(sub_plain[i]) ^ my_IDEA.encrypt(int(prev_cipher))
        encrypted_c = my_IDEA.encrypt(sub_plain[i])

        #print(sub_plain[i], ' ', my_IDEA.encrypt(int(prev_cipher)), ' ', encrypted)

        sub_enc.append(encrypted)
        sub_enc_c.append(encrypted_c)
        # encrypted = 0
        #!!!!!prev_cipher = encrypted
        prev_cipher = sub_plain[i] #!!!!!!!!!!
        #print(prev_cipher, '\n')

    encrypted = 0
    encrypted_c = 0
    #print(sub_enc, '\n')
    for i in range(x):
        sub_enc[i] = sub_enc[i] << (x - (i + 1)) * 64
        sub_enc_c[i] = sub_enc_c[i] << (x - (i + 1)) * 64

        encrypted = encrypted | sub_enc[i]
        encrypted_c = encrypted_c | sub_enc_c[i]

    # print(encrypted.to_bytes(64, 'big').decode('ASCII'))
    #print('OUT')
    return encrypted.to_bytes(64, 'big').decode('ASCII')





def work_with_file(sc):
    flagFile = False

    while not flagFile:
        info = sc.recv(1024).decode()
        filename = input(info + ': ')
        sc.send(filename.encode())
        flagFile = (sc.recv(1024).decode() == 'True')
        if not flagFile:
            print('NO SUCH FILE! TRY ONE MORE TIME...')

    enc_session_key = int(sc.recv(1024).decode())  # in 10 ns
    session_key = myRSA.MessageDec(enc_session_key, P_KEY, Q_KEY, D_KEY, N_KEY)
    # print('this is session key: ', session_key)
    cipher = sc.recv(100000).decode()
    #print(cipher)
    sc.send('1'.encode())
    iv = sc.recv(1024).decode()
    plaintext = decrypt_text(session_key, cipher, iv)
    return plaintext


def generate_RSA_keys():
    n, e, d, p, q = myRSA.Gen(2048)  # module length
    print('RSA keys have been generated successfully\n\n')
    return n, e, d, p, q


def hasKeys():
    return (N_KEY is not None) and (E_KEY is not None) and (D_KEY is not None)


long_msg = ''
while long_msg.upper() != 'Q' and long_msg.upper() != 'QUIT':

    long_msg_txt = (
        "Please enter your message, or type:\n"
        "FILE or F - to get file from server\n"
        "GENERATE KEY or GK - to generate RSA keys\n"
        "QUIT or Q - to close the socket\n\n"
        "Enter your message Here: "
    )

    long_msg = input(long_msg_txt)
    # soc.send(long_msg.encode())
    ############################
    if long_msg.upper() == 'FILE' or long_msg.upper() == 'F':
        if hasKeys():
            client.send(long_msg.encode())
            text = work_with_file(client)
            print('\n\nANSWER:\n' + text + '\n\n')
        else:
            print('BEFORE GET FILE YOU SHOULD GENERATE KEYS!\n')
    ##
    elif long_msg.upper() == 'GENERATE KEY' or long_msg.upper() == 'GK':
        if not hasKeys():
            client.send(long_msg.encode())
            N_KEY, E_KEY, D_KEY, P_KEY, Q_KEY = generate_RSA_keys()
            client.send(str(N_KEY).encode())
            client.send(str(E_KEY).encode())
        else:
            print('YOU\'VE ALREADY GENERATED KEYS FOR RSA!')

    elif long_msg.upper() == 'Q' or long_msg.upper() == 'QUIT':
        client.send(long_msg.encode())

client.close()

# # client side:
#
# import socket
# import sys
# from Crypto.PublicKey import RSA
#
# SERVER = "DESKTOP-7FRD9J8"
# PORT = 5050
# ADDR = (SERVER, PORT)
# N_KEY = None
# E_KEY = None
# D_KEY = None
#
# soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# try:
#     soc.connect(ADDR)
#
# except TimeoutError or ConnectionResetError:
#     sys.exit("\nCould not receive a response from the server.\n"
#              "Please check the IP and PORT numbers provided.\n")
#
# except OSError or ConnectionRefusedError:
#     sys.exit("\nPlease check if the server is connected to the internet\n"
#              "and that the IP and PORT numbers are correct on both ends\n")
#
# data = ""
#
#
# def work_with_file(sc):
#     flagFile = False
#
#     while not flagFile:
#         info = sc.recv(1024).decode()
#         filename = input(info + ': ')
#         sc.send(filename.encode())
#         flagFile = (sc.recv(1024).decode() == True)
#         # print(flagFile, type(flagFile))
#
#
# def generate_RSA_keys():
#     keys = RSA.generate(2048)  # module length
#     return keys.n, keys.e, keys.d
#
#
#
# while data != "Bye":
#     try:
#         long_msg_txt = (
#             "Please enter your message, or type:\n"
#             "FILE or F - to get file from server\n"
#             "GENERATE KEY or GK - to generate RSA keys\n"
#             "QUIT or Q - to close the socket\n\n"
#             "Enter your message Here: "
#         )
#
#         long_msg = input(long_msg_txt)
#         # soc.send(long_msg.encode())
#         ############################
#         if long_msg.upper() == 'FILE' or long_msg.upper() == 'F':
#             soc.send(long_msg.encode())
#             work_with_file(soc)
#         ##
#         elif long_msg.upper() == 'GENERATE KEY' or long_msg.upper() == 'GK':
#             if N_KEY is None and E_KEY is None and D_KEY is None:
#                 soc.send(long_msg.encode())
#                 N_KEY, E_KEY, D_KEY = generate_RSA_keys()
#                 soc.send(str(N_KEY).encode())
#                 soc.send(str(E_KEY).encode())
#             else:
#                 print('You\'ve already generated keys for RSA')
#
#
#
#
#     except ConnectionResetError or ConnectionAbortedError:
#
#         print("\nThe connection was forcibly closed by the remote host\n")
#         break
#     # else:
#     #     # received message from server(1024=max bytes size)
#     #     print(f"\nThe server sent: {data}\n")
#
# # when data == "Bye"
# print("Closing the socket with the server")
# soc.close()  # close the connection

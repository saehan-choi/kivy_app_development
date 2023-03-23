
import socket
import numpy as np

HOST = ''
PORT = 8000

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
        print(len(data))
    print('끝났따')
    return data

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # client_socket, addr = server_socket.accept();

        server_socket.bind((HOST, PORT))
        server_socket.listen()

        # accept a connection

        # receive the data over the socket
        
        
        conn, addr = server_socket.accept()
        # data = b''
        data = recvall(conn)
        print(data)
        conn.close()
        
                # convert the binary data back into a numpy array
                # arr = np.frombuffer(data, dtype=np.int32)
                # arr = arr.reshape(640, 480, -1)

                # print('뭐가문제노')

                # msg = '처리완료'

                # sock.sendall(msg.encode('utf-8'))
                # conn.close()
                # close the connection

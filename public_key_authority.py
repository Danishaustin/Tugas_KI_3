import socket
import json

public_key = {
    "client1": {'e': 7, 'n': 143},
    "client2": {'e': 5, 'n': 323},
}

PKA_private_key = {'d': 411, 'n': 667}
PKA_public_key = {'e': 3, 'n': 667}


def signature_encrypt(message):
    d = PKA_private_key['d']
    n = PKA_private_key['n']

    m = pow(message, d) % n
    return m

def public_key_authority():
    host = socket.gethostname()
    server_socket = socket.socket()
    server_socket.bind((host, 12345))
    server_socket.listen(5)
    print("PKA menunggu client...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Koneksi dari {addr}")

        identity = conn.recv(1024).decode()
        print(f"Permintaan Public Key untuk: {identity}")

        if identity in public_key:
            e_encrypt = signature_encrypt(public_key[identity]['e'])
            n_encrypt = signature_encrypt(public_key[identity]['n'])
            data_to_send = {'e': e_encrypt, 'n': n_encrypt}

            conn.send(json.dumps(data_to_send).encode())
            print("Public Key telah dikirim")
        else:
            conn.send(b"Identity not found")
            print("Public Key gagal dikirim")
        conn.close()

public_key_authority()

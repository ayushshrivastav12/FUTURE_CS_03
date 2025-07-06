from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

KEY = b'ThisIsASecretKey'  # 16/24/32 bytes
IV = b'ThisIsAnIV456789'   # 16 bytes

def encrypt_file(in_file, out_file):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    data = in_file.read()
    padded_data = padder.update(data) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    out_file.write(ct)

def decrypt_file(in_file, out_file):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=backend)
    decryptor = cipher.decryptor()
    ct = in_file.read()
    padded_data = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    out_file.write(data)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def generate_strong_key():
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(b"fixed_super_secure_secret")
    return key, salt

def encrypt_file_advanced(filename, key):
    with open(filename, 'rb') as f:
        data = f.read()
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    iv = os.urandom(16)
    
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    h = hmac.HMAC(key, hashes.SHA512(), backend=default_backend())
    h.update(encrypted_data)
    mac = h.finalize()
    
    encrypted_filename = filename + '.enc'
    with open(encrypted_filename, 'wb') as f:
        f.write(salt + iv + mac + encrypted_data)
    
    return encrypted_filename

key, salt = generate_strong_key()
encrypt_file_advanced('email_spammer.py', key)
encrypt_file_advanced('email_spammer_pro.py', key)

with open('.encryption_key', 'wb') as f:
    f.write(key)

print("Encryption completed successfully!")

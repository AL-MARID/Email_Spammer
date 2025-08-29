from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes, hmac
import os
import sys

def load_encryption_key():
    with open('.encryption_key', 'rb') as f:
        return f.read()

def decrypt_and_execute(encrypted_file, key):
    with open(encrypted_file, 'rb') as f:
        data = f.read()

    salt = data[:16]
    iv = data[16:32]
    mac = data[32:96]
    encrypted_data = data[96:]

    h = hmac.HMAC(key, hashes.SHA512(), backend=default_backend())
    h.update(encrypted_data)
    try:
        h.verify(mac)
    except:
        print("Error: The encrypted file has been tampered with!")
        return False

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    exec(decrypted_data)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 auto_runner.py <script_name>")
        print("Example: python3 auto_runner.py email_spammer")
        sys.exit(1)
    
    key = load_encryption_key()
    script_to_run = sys.argv[1] + '.enc'

    if decrypt_and_execute(script_to_run, key):
        print("Run completed successfully!")
    else:
        print("Failed to run the script")

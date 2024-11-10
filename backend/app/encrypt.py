import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from dotenv import load_dotenv


# Function to generate an encryption key from a password and salt
def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


# Function to encrypt data
def encrypt_data(data: str, password: str) -> tuple:
    salt = os.urandom(16)  # Dynamically generate a random salt for each encryption
    key = generate_key(password, salt)  # Generate key from password and dynamic salt
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()
    return encrypted_data, iv, salt  # Return encrypted data, IV, and salt


# Function to decrypt data
def decrypt_data(encrypted_data: bytes, password: str, iv: bytes, salt: bytes) -> str:
    key = generate_key(password, salt)  # Regenerate key using the same password and salt
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(encrypted_data) + decryptor.finalize()).decode()


def rotate_data(encrypted_data: bytes, password: str, iv: bytes, salt: bytes) -> tuple:
    decrypted_data = decrypt_data(encrypted_data, password, iv, salt)
    load_dotenv()
    password = os.getenv("ENCRYPTION_PASSWORD")
    encrypted_data, iv, salt = encrypt_data(decrypted_data, password)
    return encrypted_data, iv, salt


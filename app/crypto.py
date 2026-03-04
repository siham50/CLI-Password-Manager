from cryptography.fernet import Fernet, InvalidToken
import os


KEY_PATH = "data/key.key"

def ensure_data_folder():
    if not(os.path.exists("data/")):
        os.makedirs("data")


def generate_key():
    key = Fernet.generate_key()
    ensure_data_folder()
    with open (KEY_PATH, "wb") as file:
        file.write(key)


def load_key():
    try:
        with open (KEY_PATH, "rb") as file:
            return file.read()
    except FileNotFoundError:
        generate_key()
        with open (KEY_PATH, "rb") as file:
            return file.read()

fernet_object = Fernet(load_key())

def encrypt_password(password : str) -> bytes:
        if not(isinstance(password, str)):
            raise TypeError
        elif password == "":
            raise ValueError
        return fernet_object.encrypt(password.encode())


def decrypt_password(encrypted_password : bytes) -> str:
        if not(isinstance(encrypted_password, bytes)):
            raise TypeError
        elif encrypted_password == b"":
            raise ValueError
        try:
            return fernet_object.decrypt(encrypted_password).decode()
        except InvalidToken:
            raise
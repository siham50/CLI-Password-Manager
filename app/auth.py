from hashlib import sha256
from getpass import getpass
import os 
import hmac

master_path = "data/master.key"

def ensure_data_folder():
    if not(os.path.exists("data/")):
        os.makedirs("data")


def master_hash():
    master_attempts = 0
    while (master_attempts < 3):
        master_pwd = getpass("Create your master password: ")
        master_pwd2 = getpass ("Re-enter the master password for confirmation: ")
        master_attempts += 1
        if hmac.compare_digest(master_pwd.strip(), master_pwd2.strip()):
            master_pwd_hash = sha256(master_pwd.strip().encode()).hexdigest()
            ensure_data_folder()
            with open (master_path, "w") as file:
                file.write(master_pwd_hash)
            return True
        else:
            print("Passwords do not match.")
    return False




def compare_hash(password : str) -> bool:
    password_hash = sha256(password.strip().encode()).hexdigest()
    with open (master_path, "r") as file:
        masterpwd_hash = file.read().strip()
    return hmac.compare_digest(password_hash, masterpwd_hash)



def auth():
    password_attempts = 0
    try:
        with open (master_path, "r") as file:
            data = file.read()
        if not data or data.strip() == "":
            return master_hash()
        else:
            while(password_attempts < 3):
                password = getpass("Enter your password: ")
                password_attempts += 1
                if compare_hash(password):
                    return True
                else:
                    print("Invalid password, Please retry.")
            return False
    except FileNotFoundError:
        return master_hash()
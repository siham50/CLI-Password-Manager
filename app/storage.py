import json
import os

json_filePath = "data/vault.json"

def ensure_data_folder():
    if not(os.path.exists("data/")):
        os.makedirs("data")


def load_data():
    try:
        with open (json_filePath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        ensure_data_folder()
        with open (json_filePath, "w") as file:
            json.dump([], file, indent=4)
        return []
    except json.JSONDecodeError:
        ensure_data_folder()
        with open (json_filePath, "w") as file:
            json.dump([], file, indent=4)
        return []


def save_data(data):
    ensure_data_folder()
    with open (json_filePath, "w") as file:
        json.dump(data, file, indent=4)


def add_entry(service : str, username : str, email : str, password : bytes) -> None:
    if not(isinstance(service, str)) or not(isinstance(username, str)) or not(isinstance(email, str)) or not(isinstance(password, bytes)):
        raise TypeError
    data = load_data()
    id = max([entry["id"] for entry in data], default=0) + 1
    entry = {"id" : id,
             "service" : service,
             "username" : username,
             "email" : email,
             "password" : password}
    data.append(entry)
    save_data(data)


def get_entry(id : int) -> dict:
    data = load_data()
    for entry in data:
        if entry["id"] == id:
            return entry
    raise ValueError("Entry not found.")


def delete_entry(id : int) -> None:
    data = load_data()
    for entry in data:
        if entry["id"] == id:
            data.remove(entry)
            save_data(data)
            return True
    return False
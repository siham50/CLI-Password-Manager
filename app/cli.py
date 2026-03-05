import auth, crypto, storage
from getpass import getpass
import time
from cryptography.fernet import InvalidToken


def menu():
    if auth.auth():
        print("Login successful. Welcome.")
        while True:
            print("1. Add password\n 2. View password\n 3. Delete password\n 4. Exit\n")
            option = input ("Choose an option: ")

            if option == "1":
                try:
                    service = input("Enter the service name: ").strip()
                    username = input("Enter the username: ").strip()
                    email = input("Enter the email: ").strip()
                    password = getpass("Enter the password: ").strip()
                    storage.add_entry(service, username, email, crypto.encrypt_password(password))
                    print("The password has been successfully added.")
                except TypeError:
                    print("Wrong input type.")
                except ValueError:
                    print("Wrong input value.")

            elif option == "2":
                service = input("Enter the service name: ").strip()
                username = input("Enter the username: ").strip()
                try:
                    entry = storage.get_entry(service, username)
                    confirmation = input("Are you sure you want to display the password [Y/N]: ").strip().upper()
                    if confirmation in ["Y", "YES"]:
                        passwd = crypto.decrypt_password(entry["password"].encode())
                        print(f"The decrypted password: {passwd}")
                        time.sleep(5)
                    elif confirmation in ["N", "NO"]:
                        print("Operation cancelled.")
                    else: 
                        print("Invalid choice.")
                except ValueError:
                    print("Entry not found or empty password")
                except TypeError:
                    print("Wrong password type.")
                except InvalidToken:
                    print("Invalid token")

            elif option == "3":
                service = input("Enter the service name: ").strip()
                username = input("Enter the username: ").strip()
                if storage.delete_entry(service, username):
                    print("The password has been successfully deleted.")
                else:
                    print("Entry not found.")
            elif option == "4":
                break
            else: 
                print("Invalid option. Try again.")
    else:
        print("You ran out of attempts. Please try later.")
        return
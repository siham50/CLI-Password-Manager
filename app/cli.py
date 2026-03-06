from app import auth, crypto, storage
from getpass import getpass
import time
from cryptography.fernet import InvalidToken
import hmac


def menu():
    if auth.auth():
        print("Login successful. Welcome.")
        while True:
            print("\n1. Add password\n"
                  "2. View password\n" 
                  "3. Delete password\n" 
                  "4. Exit\n")
            option = input ("Choose an option: ")

            if option == "1":
                try:
                    attempts = 0
                    service = input("Enter the service name: ").strip()
                    username = input("Enter the username: ").strip()
                    email = input("Enter the email: ").strip()
                    while(attempts < 3):
                        password = getpass("Enter the password: ").strip()
                        password2 = getpass("Re-enter the password: ").strip()
                        attempts += 1
                        if hmac.compare_digest(password, password2):
                            storage.add_entry(service, username, email, crypto.encrypt_password(password))
                            print("The password has been successfully added.")
                            time.sleep(3)
                            break
                        else:
                            print("Passwords do not match.")
                            time.sleep(3)
                except TypeError:
                    print("Wrong input type.")
                    time.sleep(3)
                except ValueError:
                    print("Wrong input value.")
                    time.sleep(3)

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
                        time.sleep(3)
                    else: 
                        print("Invalid choice.")
                        time.sleep(3)
                except ValueError:
                    print("Entry not found or empty password")
                    time.sleep(3)
                except TypeError:
                    print("Wrong password type.")
                    time.sleep(3)
                except InvalidToken:
                    print("Invalid token")
                    time.sleep(3)

            elif option == "3":
                service = input("Enter the service name: ").strip()
                username = input("Enter the username: ").strip()
                if storage.delete_entry(service, username):
                    print("The password has been successfully deleted.")
                    time.sleep(3)
                else:
                    print("Entry not found.")
                    time.sleep(3)
            elif option == "4":
                break
            else: 
                print("Invalid option. Try again.")
                time.sleep(2)
    else:
        print("You ran out of attempts. Please try later.")
        time.sleep(3)
        return
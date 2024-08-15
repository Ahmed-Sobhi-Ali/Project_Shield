import os
import time
from pathlib import Path
from Crypto.Cipher import AES
from logs_system import Logger
from db_operations import DataBase
from data_hashing import FileHasher
from data_shredding import FileShredder
from enc_dec_operations import AES_Cipher
from key_management_system import Authentication


# Set up logging
Logger.setup_logging()

# Set the username for logging
username = os.getenv('USERNAME', 'Unknown User')
Logger.set_username(username)

# Set hostname and display welcome message
Logger.log_action('Displaying welcome message')
hostname = 'USERNAME'
print("Welcome", os.getenv(hostname))
time.sleep(1)
print("Starting Project Shield")
time.sleep(1)

"""
Authenticate using password, preselected by the programmer.
"""
Logger.log_action('Starting authentication process')
trial = 3
while trial > 0:
    password = input("Enter your password: ")
    Logger.log_action('User attempted authentication')
    if Authentication.password_hash_comparing(password):
        Logger.log_action('User password is correct')
        print("Your password is correct.")
        break
    else:
        Logger.log_action('Wrong password attempt')
        print("Wrong password.")
        trial -= 1
    
if trial == 0:
    Logger.log_action('User failed authentication 3 times')
    print("Your password was incorrect 3 times.")
    time.sleep(1)
    print("Please, don't mess with files or they will be permanently removed.")
    exit()

"""
First, search for DB files. If not found, create a new one and save new credentials.
"""
Logger.log_action('Checking for existing database file')
if not DataBase.search_files('Project_SHIELD.db'):
    Logger.log_action('New user detected, creating database')
    print("You are a new user.")
    time.sleep(1)
    print("Starting process...")
    time.sleep(1)
    print("Creating database file...")
    cr, db = DataBase.connect_to_db()
    DataBase.create_db_tables(cr, db)
    time.sleep(1)

    Logger.log_action('Generating secret credentials')
    print("Generating your secret credentials...")
    key = AES_Cipher.key_generation()
    cipher, iv = AES_Cipher.create_cipher_iv_objects(key)
    time.sleep(1)

    Logger.log_action('Saving credentials into database')
    print("Saving credentials into database...")
    data = (key, iv)
    DataBase.insert_data(cr, db, data)
    key, iv = DataBase.get_data(cr)[0]
    time.sleep(1)

    secret_value = input("Enter your secret value to encrypt the database: ")
    db_enc_key = Authentication.generate_key_from_secret_value(secret_value)
    Authentication.DB_encryption(db_enc_key, DBfile_path=f'{Path(__file__).resolve().parent}/Project_SHIELD.db')
    Logger.log_action('Database encrypted successfully')
    time.sleep(1)

    Logger.log_action('Generating file hashes')
    print("Generating file hashes...")
    time.sleep(1)
    print("Choose files for regular integrity check.")
    path = AES_Cipher.file_path()
    files_to_hash = AES_Cipher.files_list(path)
    hash_file = 'file_hashes.txt'
    FileHasher.store_hashes(files_to_hash, hash_file)

    Logger.log_action('System setup complete')
    print("It's done. The system is ready.")
    time.sleep(1)

else:
    Logger.log_action('Database file exists, starting process')
    print("Starting process...")
    time.sleep(1)

    secret_value = input("Enter your secret value to decrypt the database: ")
    db_dec_key = Authentication.generate_key_from_secret_value(secret_value)
    Authentication.DB_decryption(db_dec_key, DBfile_path=f'{Path(__file__).resolve().parent}/Project_SHIELD.db')
    Logger.log_action('Database decrypted successfully')
    print("Database decrypted successfully.")
    time.sleep(1)

    cr, db = DataBase.connect_to_db()
    key, iv = DataBase.get_data(cr)[0]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    Logger.log_action('System is ready for operations')
    print("The system is ready.")

    db_enc_key = Authentication.generate_key_from_secret_value(secret_value)
    Authentication.DB_encryption(db_enc_key, DBfile_path=f'{Path(__file__).resolve().parent}/Project_SHIELD.db')
    time.sleep(1)

    Logger.log_action('Generating file hashes for integrity check')
    print("First, choose files for regular integrity check.")
    time.sleep(1)
    path = AES_Cipher.file_path()
    files_to_hash = AES_Cipher.files_list(path)
    hash_file = 'file_hashes.txt'
    FileHasher.compare_hashes(files_to_hash, hash_file)

# Main operation loop
while True:
    operations_list = """
    Choose your operation (1 - 5):
    1 - Encryption
    2 - Decryption
    3 - Deleting files
    4 - Check for integrity
    5 - Quit the Program
    """
    user_input = input(operations_list)
    Logger.log_action(f'User selected operation {user_input}')

    if user_input == "1":
        Logger.log_action('User chose encryption')
        path = AES_Cipher.file_path()
        enc_files = AES_Cipher.files_list(path)
        AES_Cipher.encryption(cipher, path, enc_files)
        Logger.log_action('Files encrypted successfully')
        print("Your files have been encrypted successfully.")
    elif user_input == "2":
        Logger.log_action('User chose decryption')
        path = AES_Cipher.file_path()
        enc_files = AES_Cipher.files_list(path)
        AES_Cipher.decryption(key, iv, path, enc_files)
        Logger.log_action('Files decrypted successfully')
        print("Your files have been decrypted successfully.")
    elif user_input == "3":
        Logger.log_action('User chose deleting files')
        path = AES_Cipher.file_path()
        files_to_shred = AES_Cipher.files_list(path)
        FileShredder.shred_files(files_to_shred, passes=10)
        Logger.log_action('Files deleted securely')
        print("Your selected data has been deleted securely.")
    elif user_input == "4":
        Logger.log_action('User chose integrity check')
        file_to_check = input("Enter the name of your file with absolute path: ")  # File to compare
        given_hash = input("Enter your given hash: ")  # Replace with the actual hash value
        FileHasher.compare_with_hash(file_to_check, given_hash)
        Logger.log_action('Integrity check completed')
    elif user_input == "5":
        Logger.log_action('User chose to quit the program')
        print("Thank you for using Project Shield.")
        time.sleep(1)
        exit()
    else:
        Logger.log_action('User made an invalid choice')
        print("Wrong choice.")

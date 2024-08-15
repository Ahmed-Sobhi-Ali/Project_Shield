import hashlib
import base64
from cryptography.fernet import Fernet


hash_value = "8705f283faad779527dac39b27fc41b5f1ee2b5e6d0bf4f8ae7ee1723583f52d"

class Authentication:


    @staticmethod
    def password_hash_comparing(password):
        password = password.encode("utf-8")
        hash = hashlib.sha256()
        hash.update(password)
        if hash.hexdigest() == hash_value:
            return True
        else:
            return False

    @staticmethod
    def generate_key_from_secret_value(value):
        value_bytes = value.encode('utf-8')
        sha256_hash = hashlib.sha256(value_bytes).digest()
        fernet_key = base64.urlsafe_b64encode(sha256_hash[:32])
        return fernet_key

    @staticmethod
    def DB_encryption(key, DBfile_path):
        with open(DBfile_path, "rb") as thefile:
            content = thefile.read()
            encrypted_content = Fernet(key).encrypt(content)
        with open(DBfile_path, "wb") as thefile:
            thefile.write(encrypted_content)


    @staticmethod
    def DB_decryption(key, DBfile_path):
        with open(DBfile_path, "rb") as thefile:
            content = thefile.read()
            decrypted_content = Fernet(key).decrypt(content)
        with open(DBfile_path, "wb") as thefile:
            thefile.write(decrypted_content)



"""
- key and iv generation
- encryption and decryption process
"""
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


class AES_Cipher:
    @staticmethod
    def file_path():
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory(title="Select a folder")
        return Path(folder_path)

    @staticmethod
    def files_list(folder_path: Path):
        enc_files = []
        
        def add_files_from_directory(directory: Path):
            for item in directory.iterdir():
                if item.is_file():
                    enc_files.append(item)
                elif item.is_dir():
                    add_files_from_directory(item)
        
        add_files_from_directory(folder_path)
        return enc_files

    @staticmethod
    def key_generation():
        key = get_random_bytes(32)
        return key

    @staticmethod
    def create_cipher_iv_objects(key):
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        return cipher , iv

    @staticmethod
    def encryption(cipher, file_path,enc_files):
        for file in enc_files:
            with open(f"{file}", "rb") as thefile:
                content = thefile.read()
            encrypted_content = cipher.encrypt(pad(content, AES.block_size))
            with open(f"{file}", "wb") as thefile:
                thefile.write(encrypted_content)

    @staticmethod
    def decryption(key, iv, file_path,enc_files):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        for file in enc_files:
            with open(f"{file}", "rb") as thefile:
                encrypted_content = thefile.read()
            decrypted_content = unpad(cipher.decrypt(encrypted_content), AES.block_size)
            with open(f"{file}", "wb") as thefile:
                thefile.write(decrypted_content)

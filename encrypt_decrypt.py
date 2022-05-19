from cryptography.fernet import Fernet
from dotenv import dotenv_values
import os
config = dotenv_values(".env")  
key = config.get('key')

def encode(message):
    
    try:
        f = Fernet(key)
        message = bytes(message,'utf-8')
        encrypted_data = f.encrypt(message).decode("utf-8")
    except Exception as e:
        encrypted_data = None
    return encrypted_data
        
def decode(encrypted_message):
    try:
        encrypted_message = bytes(encrypted_message,'utf-8')
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_message).decode("utf-8") 

    except Exception as e:
        decrypted_data = None
    return decrypted_data

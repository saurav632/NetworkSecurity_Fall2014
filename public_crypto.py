#!/usr/bin/python

from Crypto.PublicKey import RSA
from Crypto import Random
import ast

def encrypt_data(data, public_key):
    encrypted_data = str(public_key.encrypt(data, 32))
    return encrypted_data

def decrypt_data(encrypted_data, private_key):
    data_array = ast.literal_eval(encrypted_data)
    decrypted_data = private_key.decrypt(data_array)
    return decrypted_data

### to encrypt data more than 256 bytes, encrypt block of 256 bytes, concatenate the final blocks and then do an str() ###
### to decrypt, do ast.literal_eval() first, then you will get a tuple, the index range of this tuple will be the number of concatenated encryped blocks ###

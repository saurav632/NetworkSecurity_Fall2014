#!/usr/bin/python

from stego_public import *
from public_crypto import *
# This would use the server keypair

#### Retrieving own's public/private key pair ####
my_pub_key = open('server_pub.pem').read()
my_pub_key = RSA.importKey(my_pub_key)
my_priv_key = open('server.key','r')
my_priv_key = RSA.importKey(my_priv_key.read(), passphrase='server')
#### Retrieving own's public/private key pair ####

#### Assuming we have other's public key ####
other_pub_key = open('client_pub.pem').read()
other_pub_key = RSA.importKey(other_pub_key)
#### Assuming we have other's public key ####

img_name = raw_input("Enter the name of the embedded image file: ")

img = Image.open(img_name)

ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

len_data, encrypted_msg = extract_data(pixels,ROWS,COLUMNS,bit_pos=5,RGB='G')
print 'Type of extracted encrypted msg is: %s' % (type(encrypted_msg))
print 'Extracted encrypted msg: %s' % (encrypted_msg)
print 'Length of extracted encrypted msg: %d' % (len_data)

#### decrypt data after extraction ####
decrypted_data = decrypt_data(encrypted_msg, my_priv_key)
#### decrypt data after extraction ####
print 'Original Message is: %s' % (decrypted_data)

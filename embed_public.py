#!/usr/bin/python

#from PIL import Image
from stego_public import *
from public_crypto import *
# This would use the client keypair

#### Retrieving own's public/private key pair ####
my_pub_key = open('client_pub.pem').read()
my_pub_key = RSA.importKey(my_pub_key)
my_priv_key = open('client.key','r')
my_priv_key = RSA.importKey(my_priv_key.read(), passphrase='client')
#### Retrieving own's public/private key pair ####

#### Assuming we have other's public key ####
other_pub_key = open('server_pub.pem').read()
other_pub_key = RSA.importKey(other_pub_key)
#### Assuming we have other's public key ####

data_to_encrypt = raw_input("Enter the data to encrypt: ")
img_name = raw_input("Enter the name of the image file? ")

img = Image.open(img_name)

# These variables are used to define the boundaries of image
ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

#### multiplying data ####
#data_to_encrypt = data_to_encrypt*256
#### multiplying data ####

#### encrypt before embedding ####
print 'Length of original data: %d' % (len(data_to_encrypt))
encrypted_data = encrypt_data(data_to_encrypt, other_pub_key)
print 'Data after encryption, before embedding: %s' % (encrypted_data)
#### encrypt before embedding ####

data_byted = list(bytearray(encrypted_data))
len_data = len(data_byted)
print 'Length of encrypted data %d' % (len_data)

#### inserting length of data 8 bits at a time ####
data_byted.insert(0,(len_data & 0xFF)) # inserting the bits 0-7
data_byted.insert(0,((len_data & 0xFF00)>>8)) # inserting the bits 8-15
data_byted.insert(0,((len_data & 0xFF0000)>>16)) # inserting the bits 16-23
data_byted.insert(0,((len_data & 0xFF000000)>>24)) # inserting the bits 24-31
#### inserting length of data 8 bits at a time ####

#for i in data_byted:
#    print i
#### So, first the length of the message is embedded, then the message ####
embed_data(pixels, data_byted,ROWS,COLUMNS,row=200,column=500,bit_pos=4,RGB='G')
#### So, first the length of the message is embedded, then the message ####

new_img_name = 'modified_' + img_name[:-4] + '.png'
print '\nSaving modified image to file %s' % (new_img_name)
img.save(new_img_name,'PNG')

#!/usr/bin/python

from stego_public import *
from diffie import *

#### Hardcoded values of g, p, Sa. This acting as the initiating end ####
g = 1907
p = 784313
Sa = 160011
#### Hardcoded values of g, p, Sa. This acting as the initiating end ####

#### Public key generated from this end ####
pub_key1 = exponentiate(g, Sa, p)
#### Public key generated from this end ####

#### Embedding the first public key into the image ####
img_name = raw_input("Enter the name of the image file for embedding first key? ")
img = Image.open(img_name)
ROWS, COLUMNS = img.size
start_row, start_column = 0,0
pixels = img.load()

#### inserting pub_key1 8 bits at a time ####
l = []
l.insert(0,(pub_key1 & 0xFF)) # inserting the bits 0-7
l.insert(0,((pub_key1 & 0xFF00)>>8)) # inserting the bits 8-15
l.insert(0,((pub_key1 & 0xFF0000)>>16)) # inserting the bits 16-23
l.insert(0,((pub_key1 & 0xFF000000)>>24)) # inserting the bits 24-31
# then insert the length of 4 bytes (since 32 bits pub_key1)
l.insert(0,4)
l.insert(0,0)
l.insert(0,0)
l.insert(0,0)
#### inserting pub_key1 8 bits at a time ####

#### So, first the length of the pub_key1 is embedded, then pub_key1####
embed_data(pixels, l,ROWS,COLUMNS,bit_pos=5,RGB='G')
#### So, first the length of the pub_key1 is embedded, then pub_key1####

new_img_name = img_name[:-4] + '_diffie_1.png'
print '\nSaving modified image to file %s' % (new_img_name)
img.save(new_img_name,'PNG')
#### Embedding the first public key into the image ####

#### Extract the second public key from the embedded image ####
img_name = raw_input("Enter the name of the second public key image file: ")
img = Image.open(img_name)
ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

len_data, pub_key_bits= extract_data(pixels,ROWS,COLUMNS,bit_pos=5,RGB='G')
pub_key_bits = map(ord,pub_key_bits)
pub_key2 = (pub_key_bits[0]<<24) + (pub_key_bits[1]<<16) + (pub_key_bits[2]<<8) + (pub_key_bits[3])
print 'Extracted pub_key2: %d' % (pub_key2)

### Generate the master key ###
KEY = exponentiate(pub_key2, Sa, p)
print 'Master key is %d' % (KEY)
KEY_s = ('0'*(8-len(str(KEY))) + str(KEY))*2 # making key 16 bytes
### Generate the master key ###
#### Extract the second public key from the embedded image ####

#### Embed the image with actual data encrypted with the MASTER KEY ####
data_to_encrypt = raw_input("Enter the data to encrypt: ")
img_name = raw_input("Enter the name of the image file? ")

img = Image.open(img_name)

# These variables are used to define the boundaries of image
ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

#### increasing length to reach the entire image dimensions ####
#data_to_encrypt = data_to_encrypt*15000
#### increasing length to reach the entire image dimensions ####

#### encrypt before embedding ####
print 'Length of original data: %d' % (len(data_to_encrypt))

#### comment this out for removing encryption ####
encrypted_data = des3_encryption(KEY_s, data_to_encrypt)
print 'Data after encryption, before embedding: %s' % (encrypted_data)
#### encrypt before embedding ####

data_byted = list(bytearray(encrypted_data))
len_data = len(data_byted)

#### comment this out for removing encryption ####
'''
#### comment this out if using encryption ####
data_byted = list(bytearray(data_to_encrypt))
len_data = len(data_byted)
#### comment this out if using encryption ####
'''
print 'Length of encrypted data %d' % (len_data)

#### inserting length of data 8 bits at a time ####
data_byted.insert(0,(len_data & 0xFF)) # inserting the bits 0-7
data_byted.insert(0,((len_data & 0xFF00)>>8)) # inserting the bits 8-15
data_byted.insert(0,((len_data & 0xFF0000)>>16)) # inserting the bits 16-23
data_byted.insert(0,((len_data & 0xFF000000)>>24)) # inserting the bits 24-31
#### inserting length of data 8 bits at a time ####

#### So, first the length of the message is embedded, then the message ####
embed_data(pixels, data_byted,ROWS,COLUMNS,bit_pos=2,RGB='G')
#### So, first the length of the message is embedded, then the message ####

new_img_name = img_name[:-4] + '_diffie_data.png'
print '\nSaving modified image to file %s' % (new_img_name)
img.save(new_img_name,'PNG')
#### Embed the image with actual data encrypted with the MASTER KEY ####

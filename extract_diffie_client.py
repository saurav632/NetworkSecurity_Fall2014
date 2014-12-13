#!/usr/bin/python

from stego_public import *
from diffie import *

#### Hardcoded values of g, p and Sb. This acting as one of the communicating ends ####
g = 1907
p = 784313
Sb = 12067
#### Hardcoded values of g, p and Sb. This acting as one of the communicating ends ####

#### Public key generated from this end ####
pub_key2 = exponentiate(g, Sb, p)
#### Public key generated from this end ####

#### Extract the first public key from the embedded image ####
img_name = raw_input("Enter the name of the first public key image file: ")
img = Image.open(img_name)
ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

len_data, pub_key_bits= extract_data(pixels,ROWS,COLUMNS,bit_pos=5,RGB='G')
pub_key_bits = map(ord,pub_key_bits)
pub_key1 = (pub_key_bits[0]<<24) + (pub_key_bits[1]<<16) + (pub_key_bits[2]<<8) + (pub_key_bits[3])
print 'Extracted pub_key1: %d' % (pub_key1)

### Generate the master key ###
KEY = exponentiate(pub_key1, Sb, p)
print 'Master key is %d' % (KEY)
KEY_s = ('0'*(8-len(str(KEY))) + str(KEY))*2 # making key 16 bytes
### Generate the master key ###
#### Extract the first public key from the embedded image ####

#### Embedding the second public key into the image ####
img_name = raw_input("Enter the name of the image file for embedding second key? ")
img = Image.open(img_name)
ROWS, COLUMNS = img.size
start_row, start_column = 0,0
pixels = img.load()

#### inserting pub_key1 8 bits at a time ####
l = []
l.insert(0,(pub_key2 & 0xFF)) # inserting the bits 0-7
l.insert(0,((pub_key2 & 0xFF00)>>8)) # inserting the bits 8-15
l.insert(0,((pub_key2 & 0xFF0000)>>16)) # inserting the bits 16-23
l.insert(0,((pub_key2 & 0xFF000000)>>24)) # inserting the bits 24-31
# then insert the length of 4 bytes (since 32 bits pub_key1)
l.insert(0,4)
l.insert(0,0)
l.insert(0,0)
l.insert(0,0)
#### inserting pub_key1 8 bits at a time ####

#### So, first the length of the pub_key1 is embedded, then pub_key1####
embed_data(pixels, l,ROWS,COLUMNS,bit_pos=5,RGB='G')
#### So, first the length of the pub_key1 is embedded, then pub_key1####

new_img_name = img_name[:-4] + '_diffie_2.png'
print '\nSaving modified image to file %s' % (new_img_name)
img.save(new_img_name,'PNG')
#### Embedding the second public key into the image ####

#### Extracting data from the image ####
img_name = raw_input("Enter the name of the embedded data image file: ")

img = Image.open(img_name)

ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

len_data, encrypted_msg = extract_data(pixels,ROWS,COLUMNS,row=200,column=354,bit_pos=2,RGB='G')
print 'Type of extracted encrypted msg is: %s' % (type(encrypted_msg))
print 'Extracted encrypted msg: %s' % (encrypted_msg)
print 'Length of extracted encrypted msg: %d' % (len_data)

#### decrypt data after extraction ####
decrypted_data = des3_decryption(KEY_s, encrypted_msg)
#### decrypt data after extraction ####
print 'Original Message is: %s' % (decrypted_data)
#### Extracting data from the image ####

#!/usr/bin/python

#from PIL import Image
from stego import *

data = raw_input("Enter the data to encrypt: ")
img_name = raw_input("Enter the name of the image file? ")

img = Image.open(img_name)

# These variables are used to define the boundaries of image
ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

#### increasing size of data ####
#data = data*15000
#### increasing size of data ####

data_byted = list(bytearray(data))
len_data = len(data_byted)
data_byted.insert(0,len_data) # This inserts the length of the data at the start

#### So, first the length of the message is embedded, then the message ####
RGB='G'
bit_pos=2
embed_data(pixels, data_byted,ROWS,COLUMNS,bit_pos,RGB)
#### So, first the length of the message is embedded, then the message ####

new_img_name = RGB + str(bit_pos) + img_name[:-4] + '.png'
print '\nSaving modified image to file %s' % (new_img_name)
img.save(new_img_name,'PNG')

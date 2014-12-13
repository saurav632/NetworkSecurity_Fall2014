#!/usr/bin/python

from stego import *

img_name = raw_input("Enter the name of the embedded image file: ")

img = Image.open(img_name)

ROWS, COLUMNS = img.size
start_row, start_column = 0,0

pixels = img.load()

len_data, orig_msg = extract_data(pixels,ROWS,COLUMNS,bit_pos=2,RGB='G')
print 'Original Message is: %s' % (orig_msg)

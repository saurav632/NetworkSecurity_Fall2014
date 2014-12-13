#!/usr/bin/python

from PIL import Image

def get_bit_from_int(data,bit):
    '''
    Input: Int representation of ASCII character and the bit value to extract
    Outputs: Bit value of data at the 'bit'th position
    '''
    return ((data & (0x01 << bit)) >> bit)

def embed_data(pixels,msg,ROWS,COLUMNS,row=0,column=0,bit_pos=0,RGB='R'):
    '''
    Input: pixels is a PixelAccess object used for manipulating pixels.
           msg can be encrypted or plaintext. It is embedded byte-by-byte.
           row, column indicate the starting pixel for embedding data
           Data is embedded with MSB first order
           bit_pos specifies the bit used for embedding data
    Outputs: No explicit return
             Modifies the pixels object in place
    '''
    print 'Rows and columns in the image (%d,%d)' % (ROWS,COLUMNS)

    ### Decide which color to embed in ###
    s = 'RGB'
    color = s.find(RGB)
    ### Decide which color to embed in ###

    ### Depending on bit_pos, embedding byte changes ###
    bit_dict = {i:((1<<i)^0xFF) for i in range(8)}
    ### Depending on bit_pos, embedding byte changes ###

    #### Error-checking ####
    if row >= ROWS:
        print 'Enter a valid starting row. Exiting'
        exit(0)
    if column >= COLUMNS:
        print 'Enter a valid starting column. Exiting'
        exit(0)
    #### Error-checking ####

    for i, byte in enumerate(msg):
        row_index = row
        for j in range(8):
            row_increment,column_index = divmod((column + i*8 + j),COLUMNS)

            if row_increment != 0:
                row_index = row + row_increment
            if row_index >= ROWS:
                print 'Reached the end of image. Try again with a smaller value of starting row. Exiting now'
                exit(0)

            current_index = (row_index, column_index)

            data_bit = get_bit_from_int(byte, 7-j)
            #print 'Current value of pixel is %s' % (pixels[current_index],)
            if data_bit:
                if color == 0:
                    pixels[current_index] = (pixels[current_index][color] | (1<<bit_pos), pixels[current_index][1], pixels[current_index][2])
                elif color == 1:
                    pixels[current_index] = (pixels[current_index][0], pixels[current_index][color] | (1<<bit_pos), pixels[current_index][2])
                elif color == 2:
                    pixels[current_index] = (pixels[current_index][0], pixels[current_index][1], pixels[current_index][color] | (1<<bit_pos))
            else:
                if color == 0:
                    pixels[current_index] = (pixels[current_index][color] & bit_dict[bit_pos], pixels[current_index][1], pixels[current_index][2])
                elif color == 1:
                    pixels[current_index] = (pixels[current_index][0], pixels[current_index][color] & bit_dict[bit_pos], pixels[current_index][2])
                elif color == 2:
                    pixels[current_index] = (pixels[current_index][0], pixels[current_index][1], pixels[current_index][color] & bit_dict[bit_pos])

            #print 'Changed value of pixel is %s' % (pixels[current_index],)

def extract_data(pixels,ROWS,COLUMNS,row=0,column=0,bit_pos=0,RGB='R'):
    '''
    Input: pixels is a PixelAccess object used for manipulating pixels.
           row, column indicate the starting pixel for embedded data
           First byte of embedded data indicated the length of data
           bit_pos specifies the bit used for embedding data
    Outputs: Returns the original test message
    '''

    ### Decide which color to embed in ###
    s = 'RGB'
    color = s.find(RGB)
    ### Decide which color to embed in ###

    #### Error-checking ####
    if row >= ROWS:
        print 'Enter a valid starting row. Exiting'
        exit(0)
    if column >= COLUMNS:
        print 'Enter a valid starting column. Exiting'
        exit(0)
    #### Error-checking ####

    #### First extract length of message ####
    l1,l2,l3,l4 = [[] for k in range(4)] # create 4 empty lists with l4 holding the LSB bits
    for i in range(8):
        l1.append(get_bit_from_int(pixels[row,i][color],bit_pos))
    for i in range(8):
        l2.append(get_bit_from_int(pixels[row,8+i][color],bit_pos))
    for i in range(8):
        l3.append(get_bit_from_int(pixels[row,16+i][color],bit_pos))
    for i in range(8):
        l4.append(get_bit_from_int(pixels[row,24+i][color],bit_pos))
    print l1,l2,l3,l4

    len_data = (int(''.join(map(str,l1)), 2) <<24) + (int(''.join(map(str,l2)), 2) <<16) + (int(''.join(map(str,l3)), 2) <<8) + int(''.join(map(str,l4)), 2)
    print 'Length of embedded data is %d' % (len_data)
    #### extract length of message ####

    #### Extract the message ####
    #### Extract the message ####
    data_byted = []
    for i in range(len_data):
        l = []
        row_index = row
        for j in range(8):
            row_increment,column_index = divmod((32 + (column + i*8 + j)),COLUMNS) # changing 8 to 32

            if row_increment != 0:
                row_index = row + row_increment
            if row_index >= ROWS:
                print 'Reached the end of image. Try again with a smaller value of starting row. Exiting now'
                exit(0)

            current_index = (row_index, column_index)
            l.append(get_bit_from_int(pixels[current_index][color],bit_pos))

        data_byted.append(int(''.join(map(str,l)),2))

    orig_msg = ''.join(map(chr, data_byted))
    return (len_data, orig_msg)

#!/usr/bin/python

ROWS,COLUMNS = (2880, 1800)
row = 2878
column = 1750
row_increment = 0
for i in range(12):
    row_index = row
    for j in range(8):
        row_increment,column_index = divmod((column + i*8 + j),COLUMNS)

        if row_increment != 0:
            row_index = row + row_increment

        if row_index >= ROWS:
            print 'REached end of image. Exiting'
            exit(0)
        print "(%d,%d)" % (row_index,column_index)

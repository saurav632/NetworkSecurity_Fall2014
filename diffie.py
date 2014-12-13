#!/usr/bin/python

from Crypto.Cipher import DES3

def exponentiate(m, d, n):
    """
    This function calculates (m raised to the power of d) mod n
    and returns the remainder
    """

    result = 1           # initialize the result value to 1

    bin_digit_d = len(list(bin(d))[2:])

    binary_d = list(bin(d))[2:] # returns a list of 0s and 1s but in <str> type
    #print 'The binary representation of d is:', binary_d

    for digit in binary_d:
        result = result*result
        result = result % n
        if int(digit) == 1:
            result = result * m

        #print 'Intermediate value of result:', result
        result = result % n         # result mod n
        #print 'At the end of iteration, after mod, result:', result

    #print 'final result is:', result
    return result

def des3_encryption(key, msg):
    # pad msg for 8-byte alignment
    IV = '12345678'

    r = len(msg)%8
    if r:
        msg = msg + ":" + 'A'*(7-r)
        # use a different delimiter to identify padding
    
    des_key = DES3.new(key, DES3.MODE_CBC, IV)
    return des_key.encrypt(msg)

def des3_decryption(key, msg):
    IV = '12345678'

    des_key = DES3.new(key, DES3.MODE_CBC, IV)
    msg_pad = des_key.decrypt(msg)

    # remove padding after decryption
    temp = msg_pad.rsplit(":", 1)
    original_msg = str(temp[0])
    return original_msg


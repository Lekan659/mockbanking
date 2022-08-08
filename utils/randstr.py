"""Unique keys is a library that helps to generate distint keys, reference no. 
    ids for primary record identification.
"""
import random

def get_otp(length=8):
    chars = [0,1,2,3,4,5,6,7,8,9]
    otp = ''
    for index in range(0,length):
        otp += str(chars[random.randint(0,9)])
    return otp

def get_token(length=16):
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            0,1,2,3,4,5,6,7,8,9]
    token = ''
    for index in range(0,length):
        token += str(chars[random.randint(0, len(chars)-1)])
    return token
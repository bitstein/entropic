#!/usr/bin/python3
import binascii
import csv
import hashlib
import sys

dicerolls = sys.argv[1]

def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

dicerolls = split(dicerolls, 5)

dicewords = ''

for roll in dicerolls:
    with open('Dice List.csv') as file:
        for line in file:
            number = line[:5]
            word = line[6:].strip()
            if roll == number:
                dicewords = ''.join((dicewords, word))

private_key = dicewords.encode('ascii')
private_key = hashlib.sha256(private_key).digest()
private_key = binascii.hexlify(private_key)
private_key = private_key.decode('utf-8')
print("Back up phrase: " + dicewords)
print("Private key: " + private_key)

#!/usr/bin/python3
import binascii
import csv
import hashlib
import sys

# By Filioo Valsorda: https://filippo.io/brainwallets-from-the-password-to-the-address/
def encodeWIF(private_key):
    # Prepend the 0x80 version/application byte
    private_key = b'\x80' + binascii.unhexlify(private_key)
    # Append the first 4 bytes of SHA256(SHA256(private_key)) as a checksum
    private_key += hashlib.sha256(hashlib.sha256(private_key).digest()).digest()[:4]
    # Convert to Base58 encoding
    code_string = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    value = int.from_bytes(private_key, byteorder='big')
    output = ""
    while value:
        value, remainder = divmod(value, 58)
        output = code_string[remainder] + output
    return output

def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

worddict = {}

with open('Dice List.csv') as file:
    for line in file:
        worddict[line[:5]] = line[6:].strip()

dicerolls = sys.argv[1]

dicerolls = split(dicerolls, 5)

dicewords = ''

for roll in dicerolls:
     dicewords = ' '.join((dicewords, worddict[roll]))

private_key = dicewords.encode('ascii')
private_key = hashlib.sha256(private_key).digest()
private_key = binascii.hexlify(private_key)
private_key = private_key.decode('utf-8')
print("Back up phrase: '" + dicewords + "'")
print("Private key: " + private_key)
print("Private key (WIF): " + encodeWIF(private_key))

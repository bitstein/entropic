#!/usr/bin/python3
import binascii
import csv
import hashlib
import sys
import argparse

def load_worddict():
    worddict = {}

    with open('Dice List.csv') as file:
        for line in file:
            worddict[line[:5]] = line[6:].strip()
    return worddict

def split(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]

def phrase_to_privkey(phrase):
    privkey = phrase.encode('ascii')
    privkey = hashlib.sha256(privkey).digest()
    privkey = binascii.hexlify(privkey)
    return privkey.decode('utf-8')

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

def numaddrs_type(str):
    x = int(str)
    if x < 1:
        msg = "Number of addresses must be greater than 0."
        raise argparse.ArgumentTypeError(msg)
    return x

def print_addr(phrase, key):
    print()
    print("Back up phrase: '" + phrase + "'")
    print("Private key: " + key)
    print("Private key (WIF): " + encodeWIF(key))

def main():
    worddict = load_worddict()

    parser = argparse.ArgumentParser(description='Generate diceware addresses.')
    parser.add_argument('dicerolls', help='dice rolls - no spaces')
    parser.add_argument('-n','--numaddrs', nargs='?', help="Number of diceware addresses (>= 1)", type=numaddrs_type)
    args = parser.parse_args()
    
    dicerolls = args.dicerolls
    dicerolls = split(dicerolls, 5)
    dicewords = ''

    for roll in dicerolls:
        dicewords = ' '.join((dicewords, worddict[roll]))

    dicewords = dicewords.strip()

    private_key = phrase_to_privkey(dicewords)
    print_addr(dicewords, private_key)

    if (args.numaddrs and args.numaddrs > 1):
        for i in range(1, args.numaddrs):
            dicewordsnum = dicewords + str(i)
            private_key = phrase_to_privkey(dicewordsnum)
            print_addr(dicewordsnum, private_key)

    print()

if __name__ == '__main__':
    main()
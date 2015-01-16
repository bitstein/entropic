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

def dicerolls_type(str):
    try:
        x = int(str)
    except:
        msg = "Dicerolls must only include integers."
        raise argparse.ArgumentTypeError(msg)

    for s in str:
        if int(s) < 1 or int(s) > 6:
            msg = "Each die roll must be a number 1-6."
            raise argparse.ArgumentTypeError(msg)

    remainder = len(str) % 5
    if not remainder == 0:
        msg = "Each word must be five dicerolls. Roll a die {0} more times.".format(5-remainder)
        raise argparse.ArgumentTypeError(msg)
    return str

def numaddrs_type(str):
    try:
        x = int(str)
    except:
        msg = "Number of addresses must be an integer."
        raise argparse.ArgumentTypeError(msg)

    if x < 1:
        msg = "Number of addresses must be greater than 0."
        raise argparse.ArgumentTypeError(msg)
    return x

def print_addr(phrase, key):
    print()
    print("Back up phrase: '" + phrase + "'")
    print("Private key: " + key)
    print("Private key (WIF): " + encodeWIF(key))

def get_parser():
    parser = argparse.ArgumentParser(description='Generate diceware addresses.')
    parser.add_argument('dicerolls', help='dice rolls - no spaces', type=dicerolls_type)
    parser.add_argument('-n','--numaddrs', nargs='?', help="Number of diceware addresses (>= 1)", type=numaddrs_type)
    parser.add_argument('-s','--salt',nargs='?', help="Add a salt (quotation marks are optional, unless salt includes spaces; use escape character for quotation marks in salt)")
    return parser.parse_args()

def main():
    worddict = load_worddict()

    args = get_parser()
    
    dicerolls = args.dicerolls
    dicerolls = split(dicerolls, 5)
    dicewords = ''

    for roll in dicerolls:
        dicewords = ' '.join((dicewords, worddict[roll]))

    dicewords = dicewords.strip()

    if args.salt:
        dicewords += ' ' + args.salt.strip()

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
import binascii
import os
import sys
import glob

# get the name of the newly downloaded file
def newest_file():
    list_of_files = glob.glob(os.path.expanduser('~')+"/Downloads/*")  # goes to the user's root directory
    latest_file = max(list_of_files, key=os.path.getmtime)      #most recent file in the directory
    return latest_file

#get a string of hexadecimals of a file
def get_hex(file):
    with open(file, 'rb') as f:
        content = f.read()
    hex1 = binascii.hexlify(content)
    str_hex = str(hex1)[2:-1] # get rid of first 2 and last 1 characters
    return str_hex

def make_substrings(size, file):
    i = 0
    substrings = []
    while i < len(file) - sizeof_substring - 1:
        #file might be a keyword so may need to change that variable name
        substrings.append(file[i:i+sizeof_substring])
        i+=1
    return substrings

viruses=["virus1.txt", "virus2.txt", "virus3.txt"]

for virus in viruses:
    # have to unzip it first for our real files
    virus = get_hex(virus)
    sizeof_substring = 5
    substrings = make_substrings(sizeof_substring, virus)
    downloaded = newest_file()
    print(downloaded)
    downloaded = get_hex(downloaded)
    i = 0
    while i < len(downloaded) - sizeof_substring - 1:
        if downloaded[i:i+sizeof_substring] in substrings:
            print("this is a virus")
            sys.exit(0)
        i += 1

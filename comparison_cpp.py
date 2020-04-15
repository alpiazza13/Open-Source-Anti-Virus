
import binascii
import os
import sys
import glob
import subprocess

def compress(s):
    #can find better compression but really has to keep the linear pattern, so most compressions don't work
    # so i feel like what i'm doing if pretty good cause i divide size by a number and keep linear pattern
    i = 0
    result = ""
    while i < len(s):
        if i % 19 == 0:
            result += str(s[i])
        i+=1
    return result


# get the name of the newly downloaded file
def newest_file():
    list_of_files = glob.glob(os.path.expanduser('~')+"/Downloads/*")  # goes to the user's root directory
    latest_file = max(list_of_files, key=os.path.getmtime)      #most recent file in the directory
    return latest_file

#get a string of hexadecimals of a file
def get_hex_compressed(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    hex1 = compress(binascii.hexlify(content))
    str_hex = str(hex1)[2:-1] # get rid of first 2 and last 1 characters
    return str_hex


def make_substrings(size, file):
    i = 0
    substrings = []
    while i < len(file) - size - 1:
        substrings.append(file[i:i+size])
        i+=1
    return substrings


def compare(hex_file, hex_virus, sub_size):
    if sub_size > len(hex_file) or sub_size > len(hex_virus) :
        return False
    hex_file_subs = make_substrings(sub_size, hex_file)
    if any(hex_sub in hex_virus for hex_sub in hex_file_subs):
        return True
    return False


viruses=["virus1.txt", "virus2.txt", "virus3.txt", "try.jpg"]
latest_download = newest_file()
download_hex = get_hex_compressed(latest_download)

viruses_lst = []
for virus in viruses :
    virus_string = get_hex_compressed(virus)
    viruses_lst.append(virus_string)

os.system("g++ compute.cpp")  #compiling my cpp script, don't wanna do it in the loop

def tunnel_a_value(value, tunnelnb):
    f = open("tunnel" + str(tunnelnb) +".txt" ,"w")
    if type(value) == list:
        for x in value:
            f.write(str(x) + " ")
    else :
        f.write(str(value))
    f.close()

final_subsize = 200
tunnel_a_value(viruses_lst,1)
tunnel_a_value(download_hex,2)
tunnel_a_value(final_subsize,3)

os.system("./a.out")
f = open("tunnel1.txt","r")
result = f.read()

'''
Our number final_subsize is the threshold from which if a file an han equal substrings of this size with a
virus, then it can be a virus
200 -> 8kB
'''

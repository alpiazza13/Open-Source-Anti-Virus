import binascii
import os
import sys
import glob
import random
from helpers import notify, compare, newest_file, get_hex_compressed, size_downloads
import time


viruses=["virus1.txt", "virus2.txt", "virus3.txt", "try.jpg"]
latest_download = newest_file()
download_hex = get_hex_compressed(latest_download)

viruses_dict = {}
for virus in viruses:
    virus_string = get_hex_compressed(virus)
    viruses_dict[virus] = virus_string

#check if hex_file is a virus
def is_virus(hex_file, viruses_str, final_subsize):  #final_subsize has to be carefully evaluated
    for virus in viruses_str:
        # print(virus)
        sub_size = 16 #arbitrary small number
        go_on = True
        while go_on:
            if sub_size >= final_subsize:
                return True
            result = compare(hex_file, viruses_str[virus], sub_size)
            # print("compare", sub_size, result)
            if result == False:
                go_on = False
            sub_size *= 2 # kind of arbitrary
    return False


def main():
    newest = newest_file()
    size_folder = size_downloads()
    while True:
        checkfornew = newest_file()
        new_size_folder = size_downloads()
        time.sleep(0.5)
        if new_size_folder >= size_folder:      #check if the new most recent is not due to a deletion
            if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
                if checkfornew != newest:
                    result = is_virus(checkfornew, viruses_dict, 200)
                    if result == True:
                        notify("VIRUS ALERT", "this is probably a virus, you should delete it!")
                    else:
                        notify("VIRUS CHECK", "this is probably a virus, you should delete it!")
        if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
            newest = checkfornew
        size_folder = new_size_folder

main()

'''
Our number final_subsize is the threshold from which if a file an han equal substrings of this size with a
virus, then it can be a virus
200 -> 8kB
128 * 20 * 2 bytes = about 5kB
'''

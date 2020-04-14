
import binascii
import os
import sys
import glob


def compress(s):
    #can find better compression but really has to keep the linear pattern, so most compressions don't work
    # so i feel like what i'm doing if pretty good cause i divide size by a number and keep linear pattern
    i = 0
    result = ""
    while i < len(s):
        if i % 20 == 0:
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


def make_substrings(size, filename):
    i = 0
    substrings = []
    while i < len(filename) - size - 1:
        substrings.append(filename[i:i+size])
        i+=1
    return substrings

viruses=["virus1.txt", "virus2.txt", "virus2.txt","virus2.txt","virus2.txt","virus2.txt","virus2.txt","virus2.txt","virus2.txt","virus2.txt","virus2.txt","virus3.txt", "try.jpg"]
latest_download = newest_file()
download_hex = get_hex_compressed(latest_download)
print(len(download_hex))
print(latest_download)

def compare(hex_file, hex_virus, sub_size):
    if sub_size > len(hex_file) or sub_size > len(hex_virus) :
        return False
    hex_file_subs = make_substrings(sub_size, hex_file)
    if any(hex_sub in hex_virus for hex_sub in hex_file_subs):
        return True
    return False


# based on idea that smaller substrings make it way faster, we go from ground up
# cause most of them will be different with small substrings, and we only check for bigger
# substrings when the files are very similar
# We'll do a lot more work for similar files but it will be exponentially faster for different files
def is_virus(hex_file, viruses, final_subsize):  #final_subsize has to be carefully evaluated
    for virus in viruses:
        print(virus)
        sub_size = 150 # we can start with however small, the smallest just means a little more computing
                      #but faster if file really really different
        go_on = True
        virus = get_hex_compressed(virus)
        while go_on:
            if sub_size >= final_subsize:
                return True
            result = compare(hex_file, virus, sub_size)
            print("compare", sub_size, result)
            if result == False :
                go_on = False
            sub_size *= 2 # *= whatever we want
    return False

print(is_virus(download_hex, viruses, 200 ))

'''
Our number final_subsize is the threshold from which if a file an han equal substrings of this size with a
virus, then it can be a virus
200 -> 8kB
'''

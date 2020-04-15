import binascii
import os
import sys
import glob
import random


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


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

viruses=["virus1.txt", "virus2.txt", "virus3.txt", "try.jpg"]
latest_download = newest_file()
download_hex = get_hex_compressed(latest_download)

def compare(hex_file, hex_virus, sub_size):
    if sub_size > len(hex_file) or sub_size > len(hex_virus):
        return False
    # hex_file_subs = make_substrings(sub_size, hex_file)
    # if any(hex_sub in hex_virus for hex_sub in hex_file_subs):
    #     return True
    # return False
    hex_file_subs = make_substrings(sub_size, hex_file)
    hex_virus = make_substrings(sub_size, hex_virus)
    hex_file_subs = set(hex_file_subs)
    hex_virus = set(hex_virus)
    return len(hex_file_subs.intersection(hex_virus)) > 0


# based on idea that smaller substrings make it way faster, we go from ground up
# cause most of them will be different with small substrings, and we only check for bigger
# substrings when the files are very similar
# We'll do a lot more work for similar files but it will be exponentially faster for different files

#Let's just compress and get hex of viruses before so that we don't have to do it when a file is downloaded
#it saves time from donwload to result of virus or not


viruses_dict = {}
for virus in viruses :
    virus_string = get_hex_compressed(virus)
    viruses_dict[virus] = virus_string

def generate_str(size):
    s = ""
    for x in range(size):
        s += str(random.randint(0,9))
    return s

big = generate_str(100000)

viruses_dict["big"] = big


#We're gonna have to put thing in an infinite loop that checks if a file has been downloaded and
#runs the function if yes
def is_virus(hex_file, viruses_str, final_subsize):  #final_subsize has to be carefully evaluated
    for virus in viruses_str:
        print(virus)
        sub_size = 16 # we can start with however small, the smallest just means a little more computing
                      #but faster if file really really different
        go_on = True
        while go_on:
            if sub_size >= final_subsize:
                return True
            result = compare(hex_file, viruses_str[virus], sub_size)
            print("compare", sub_size, result)
            if result == False :
                go_on = False
            sub_size *= 2 # *= whatever we want
    return False

if is_virus(viruses_dict["big"], viruses_dict, 200):
    notify("VIRUS ALERT", "this is probably a virus, you should delete it!")

# print(is_virus(viruses_dict["big"], viruses_dict, 2000 ))


'''
Our number final_subsize is the threshold from which if a file an han equal substrings of this size with a
virus, then it can be a virus
200 -> 8kB
128 * 20 * 2 bytes = about 5kB
'''

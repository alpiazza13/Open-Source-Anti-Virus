import binascii
import os
import sys
import glob
import random



#makes pop-up
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
#
def alert(status):
    if status == "virus":
        os.system(""" osascript -e 'display dialog "THIS IS PROBABLY A VIRUS! Do you want us to delete the file for you? " buttons {"Yes ","No"} with title "VIRUS CHECK" with icon Stop'
        """)
    else:
        os.system("""
                    osascript -e 'display dialog "You are all good, this is most likely not a virus" buttons {"OK"} with title "VIRUS CHECK" with icon Note'
        """)

def compress(s):
    i = 0
    result = ""
    while i < len(s):
        if i % 20 == 0:
            result += str(s[i])
        i+=1
    return result


# get name of most recent file in downloads
def newest_file():
    list_of_files = glob.glob(os.path.expanduser('~')+"/Downloads/*")
    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file

def size_downloads():
    return len(os.listdir(os.path.expanduser('~')+"/Downloads"))

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

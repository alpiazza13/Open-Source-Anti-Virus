import binascii
import os

def compress(s):
    i = 0
    result = ""
    while i < len(s):
        if i % 20 == 0:
            result += str(s[i])
        i+=1
    return result

#get a string of hexadecimals of a file
def get_hex_compressed(filename):
    file_bin = open(filename, 'rb')
    file_content = file_bin.read()
    #hex_dump = file_content.hex()
    hex_dump = binascii.hexlify(file_content)
    compressed_hex_dump = compress(hex_dump)
    return compressed_hex_dump

def make_substrings(size, filename):
    i = 0
    substrings = []
    while i < len(filename) - size - 1:
        substrings.append(filename[i:i+size])
        i+=1
    return substrings

def fit_to_unix(filename):
    newname = ""
    for char in filename:
        if char == " " or char == "(" or char == ")":
            newname += "\\" + char
        else :
            newname += char
    return newname

# unpack nested directories to obtain all files -- will be useful for scanning files in folders
def unpack_folder(directory):
    all_dir_files = [] 
    try:
        dir_files = os.walk(directory)
        for each_folder in list(dir_files):
            for each_file in each_folder[2]:
                full_dir = "{}/{}".format(each_folder[0],each_file)
                if os.path.isfile(full_dir):
                    all_dir_files.append(full_dir)
        return all_dir_files
    except:
        return all_dir_files

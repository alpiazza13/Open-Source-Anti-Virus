import binascii
import os
import hashlib

def split_list(l, n):
    avg = len(l) / n
    out = []
    last = 0
    while last < len(l):
        out.append(l[int(last):int(last + avg)])
        last += avg
    return out
# print(split_list([1,2,3,4,5,6,7,8], 6))

# assumes len(d) >= n
def split_dict(d, n):

    keys = list(d.keys())
    key_groups = split_list(keys, n)
    dicts = []
    for key_group in key_groups:
        this_dict = {}
        for key in key_group:
            this_dict[key] = d[key]
        dicts.append(this_dict)

    return dicts

# a_dict = {number: number for number in range(11)}
# print(split_dict(a_dict, 2))

def compress(s):
    i = 0
    result = ""
    while i < len(s):
        if i % 20 == 0:
            result += str(s[i])
        i+=1
    return result

#get a string of hexadecimals of a file
def get_hex_compressed(filename, compress_bool=True):
    file_bin = open(filename, 'rb')
    file_content = file_bin.read()
    #hex_dump = file_content.hex()
    hex_dump = binascii.hexlify(file_content)
    # decode hext dump from binary object to string
    hex_dump = hex_dump.decode('utf-8')
    # compress if compress_bool is True
    if compress_bool:
        hex_dump = compress(hex_dump)
    return hex_dump

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

# md5 hash of a file with bloksize. Takes a file and returns md5 checksum of file
def md5_filehash(filename):
    if os.path.getsize(filename)/(10**6) > 50: #read file in chunks if size > 50 mb
        blocksize = 1024
        filehash = hashlib.md5()
        bin_fileobj = open(filename, 'rb')
        buf = bin_fileobj.read(blocksize)
        while len(buf) > 0:
            filehash.update(buf)
            buf = bin_fileobj.read(blocksize)
        return filehash.hexdigest()
    else:
        filehash = hashlib.md5()
        bin_fileobj = open(filename, 'rb')
        buf = bin_fileobj.read()
        filehash.update(buf)
        return filehash.hexdigest()

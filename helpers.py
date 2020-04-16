import binascii

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


def formating_viruses(viruses):
    viruses_dict = {}
    for virus in viruses:
        virus_string = get_hex_compressed(virus)
        viruses_dict[virus] = virus_string
    return viruses_dict


def fit_to_unix(filename):
    newname = ""
    for char in filename:
        if char == " " or char == "(" or char == ")":
            newname += "\\" + char
        else :
            newname += char
    return newname

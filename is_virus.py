from helpers import make_substrings

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




'''
Our number final_subsize is the threshold from which if a file an han equal substrings of this size with a
virus, then it can be a virus
200 -> 8kB
128 * 20 * 2 bytes = about 5kB
'''

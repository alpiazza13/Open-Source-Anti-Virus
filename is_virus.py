from helpers import make_substrings, get_hex_compressed, md5_filehash, split_dict
import multiprocessing as mp


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



# check if hex_file is a virus
# for no multiprocessing
def is_virus(hex_file, viruses, final_subsize):  #final_subsize has to be carefully evaluated
    for virus in viruses:
        sub_size = 16 #arbitrary small number
        go_on = True
        while go_on:
            if sub_size >= final_subsize:
                return True
            result = compare(hex_file, viruses[virus]["hexdump"], sub_size)
            # print("compare", sub_size, result)
            if result == False:
                go_on = False
            sub_size = sub_size * 2 # kind of arbitrary
    return False

#multiprocessing version
def is_virus_multi(hex_file, viruses, final_subsize, return_dict, process_nb):  #final_subsize has to be carefully evaluated
    final_result = False
    for virus in viruses:
        sub_size = 16 #arbitrary small number
        go_on = True
        while go_on:
            if sub_size >= final_subsize:
                final_result = True
            result = compare(hex_file, viruses[virus]["hexdump"], sub_size)
            # print("compare", sub_size, result)
            if result == False:
                go_on = False
            sub_size = sub_size * 2 # kind of arbitrary
    return_dict[str(process_nb)] = final_result


def multiprocess_check(hex_file, viruses, final_subsize):
    manager = mp.Manager()
    return_dict = manager.dict()
    list_processes = []
    viruses_divided = split_dict(viruses,mp.cpu_count()+1)
    # starting processes
    process_nb = 0
    for portion in viruses_divided:
        p = mp.Process(target=is_virus_multi, args = (hex_file, portion, final_subsize, return_dict, process_nb,))
        list_processes.append(p)
        p.start()
        process_nb += 1
    # waiting for all processes to be done
    for portion in list_processes:
        portion.join()

    if True in return_dict.values():
        return True
    else :
        return False

'''
Our number final_subsize is the threshold from which if a file an han equal substrings of this size with a
virus, then it can be a virus
200 -> 8kB
128 * 20 * 2 bytes = about 5kB
'''

# method of determining if file is virus by analyzing how many of the the the pattern of intersection of strings in both file being scanned and virusfile
def split_string(filefile):
    filefile_split = ""
    i = 0
    j = 0
    while i < len(filefile):
        if j == 4:
            filefile_split += " "
            j = 0
        else:
            filefile_split += str(filefile[i])
            i += 1
            j += 1
    filefile_split = filefile_split.split(' ')
    return filefile_split

'''
This function is_virus_v2(virusfile : string, file : string) : bool computes the file virus metric based on the length of substrings found in both virus and file being scanned.
First, the function splits the hex strings of file and virus into chunks of length 4. Why 4? Because I decided that 4 is an approximate length of a hex string that represents something meaningful in a file. For example, if hex string of our file was 'abcdeabcdabcdfgh', the resulting string would be 'abcd abcd efgh'
Next, we split the resulting string at the whitespaces. 'abcd abcd abcd efgh': str -> ['abcd', 'abcd', 'abcd', 'efgh'] : str list
Next, we compute the intersection of chunks in both virus and file being scanned
Example: If the representation of file was ['abcd', 'abcd', 'efgh'] as above and the virus was ['abcd', 'abcd', 'abcd', 'efgh'], we'll have:
intersection(file: set, virus: set) -> ['abcd', 'efgh'] : set. At this point, if the intersection is awfully similar to virus or file, then we flag the file as malicious
Now we know that the chunks (substrings) in both the virus and the file are ['abcd', 'efgh'].
Next, we analyze the positions of the strings. We initialize a counter to track strings that repeat in a contiguous manner in both the virus and file, i.e., a contiguous subsequence
Our file = ['abcd', 'abcd', 'efgh'], virus = ['abcd', 'abcd', 'abcd', 'efgh']
We see that the first item ('abcd') in the intersection is actually a contiguous subsequence that is counted 2 times. The second is counted once. We consider the maximum number of counted instances of contiguous subsequences = m, m ∈ {ℤ:[0,max(N_virus_string, N_file_string)]}
To decide whether or not a file is a virus, we calculate a virus metric v that is:
 v => m / min(N_virus_string, N_file_string), where v ∈ {ℤ:[0,min(N_virus_string, N_file_string)].
 v => m / min(len(virus_string), len(file_string))
The proper bound of the virus metric v is really just 0 <= v <= 1, 0 being "not a virus" and 1 being "run for your dear life"
A simple proof to show this works. If file is the same as virus, then m = 1, and min(len(virus_string),len(file_string)) = 1. Hence in this case this

Currently, I have decided that the threshold would be 0.3. A file is considered dangerous if v > 0.3

This function also checks the obvious good old way lame way of checking if filehash of file corresponds to filehash of virus

'''

def is_virus_v2(filefile,viruses,threshold=0.33):
    file_hex_str = get_hex_compressed(filefile, compress_bool=False)
    filefile_split = split_string(file_hex_str)
    all_seq_count = []
    for virus_key in viruses:
        # check if checksum of file is same as checksum of of virus
        if md5_filehash(filefile) == viruses[virus_key]["md5hash"]:
            return True
        virusfile_split = viruses[virus_key]["hexdump"].split(' ')
        intersection = set(virusfile_split).intersection(set(filefile_split))
        # if there length of instersection is too close to the (length(virus), length(file))
        # print(len(intersection),len(filefile_split),len(virusfile_split))
        file_seq_count = [0]
        for each in intersection:
            pos_virusfile_split = virusfile_split.index(each)
            pos_filefile_split = filefile_split.index(each)
            seq_count = 1
            try:
                while (virusfile_split[pos_virusfile_split+1] == filefile_split[pos_filefile_split+1]):
                    seq_count += 1
                    pos_virusfile_split += 1
                    pos_filefile_split += 1
                    if (seq_count / min(len(virusfile_split),len(filefile_split))) > threshold:
                        return True
            except:
                pass
            file_seq_count.append(seq_count)
            virus_metric = seq_count / min(len(virusfile_split),len(filefile_split))
            if (virus_metric > threshold):
                return True

        all_seq_count.append(file_seq_count)
        virus_metric = max(file_seq_count) / min(len(virusfile_split),len(filefile_split))
        if (virus_metric > threshold):
            return True

    virus_metric = max(list(map(max, all_seq_count))) / min(len(virusfile_split),len(filefile_split))
    if (virus_metric > threshold):
        return True
    return False

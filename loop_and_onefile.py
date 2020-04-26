import time
from os_functions import alert, newest_file, size_downloads
from is_virus import is_virus
from helpers import formating_viruses, get_hex_compressed

'''

To get the viruses for the online github repo, we need to do the following
When we eventually link, we have to make sure clonning the virus is something safe to do!!!!

from get_viruses import get_viruses_github
viruses = get_viruses_github()

'''
viruses = ["viruses/virus1.txt", "viruses/virus2.txt", "viruses/virus3.txt", "viruses/try.jpg"]

viruses_dict = formating_viruses(viruses)

def main_loop():
    newest = newest_file()
    size_folder = size_downloads()
    while True:
        checkfornew = newest_file()
        new_size_folder = size_downloads()
        time.sleep(0.5)
        if new_size_folder >= size_folder:      #check if the new most recent is not due to a deletion
            if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
                if checkfornew != newest:
                    result = is_virus(get_hex_compressed(checkfornew), viruses_dict, 200)
                    if result == True:
                        alert("virus", checkfornew)
                    else:
                        alert("not_virus", checkfornew)
        if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
            newest = checkfornew
        size_folder = new_size_folder

def one_file(filename):
    result = is_virus(get_hex_compressed(filename), viruses_dict, 200)
    if result == True:
        alert("virus", filename)
    else:
        alert("not_virus", filename)

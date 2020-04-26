import time
import os
from os_functions import alert, newest_file, size_downloads
from is_virus import is_virus
from helpers import get_hex_compressed, unpack_folder


# generating virus dictionary. This is saved to file as a json instead to save time. Look at example
viruses_fileobj = open('viruses/viruses.json','r')
viruses_dict = viruses_fileobj.read()
viruses_dict = eval(viruses_dict)

'''

To get the viruses for the online github repo, we need to do the following
When we eventually link, we have to make sure clonning the virus is something safe to do!!!!

from get_viruses import get_viruses_github
viruses = get_viruses_github()

'''
# viruses = ["viruses/virus1.txt", "viruses/virus2.txt", "viruses/virus3.txt", "viruses/try.jpg"]

# viruses_dict = formating_viruses(viruses)

def main_loop():
    newest = newest_file()
    size_folder = size_downloads()
    while True:
        checkfornew = newest_file()
        new_size_folder = size_downloads()
        time.sleep(0.5)
        if new_size_folder >= size_folder:      #check if the new most recent is not due to a deletion
            directory,file_extension = os.path.splitext(checkfornew)
            # making sure latest file is actually a file (and not a folder moved from somewhere else to downloads) and isn't a .crdownload or .download file
            if os.path.isfile(checkfornew) and not file_extension in ['.crdownload','.download','.zip']:
                if checkfornew != newest:
                    result = is_virus(get_hex_compressed(checkfornew), viruses_dict, 200)
                    if result == True:
                        alert("virus", checkfornew)
                    # else no need to bother user if file is not virus

            # if newest thing is a folder (hopefully an unzipped one)                    
            elif os.path.isdir(checkfornew):
                if checkfornew != newest:
                    files_to_scan = unpack_folder(checkfornew)
                    file_status = []
                    for each in files_to_scan:
                        status = is_virus(get_hex_compressed(each), viruses_dict, 200)
                        file_status.append(status)
                    # alert if any is True
                    if any(file_status):
                        alert("virus", checkfornew)

        if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
            newest = checkfornew
        size_folder = new_size_folder

def one_file(filename):
    result = is_virus(get_hex_compressed(filename), viruses_dict, 200)
    if result == True:
        alert("virus", filename)
    else:
        alert("not_virus", filename)

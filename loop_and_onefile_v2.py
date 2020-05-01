import time
import os
import io
import requests
from os_functions import alert, newest_file, size_downloads
from is_virus import is_virus_v2, multiprocess_check_v2
from helpers import get_hex_compressed, unpack_folder
import zipfile
import dialogs


# Alternative ways of reading combined virus files
'''
viruses = ["viruses/virus1.txt", "viruses/virus2.txt", "viruses/virus3.txt", "viruses/try.jpg"]
viruses_dict = formating_viruses(viruses)

making http request to repo that lives on Sam's account to get JSON of viruses
'''

'''
To get the viruses for the online github repo, we need to do the following
When we eventually link, we have to make sure clonning the virus is something safe to do!!!!
from get_viruses import get_viruses_github
viruses = get_viruses_github()
'''

'''
file_url = "https://github.com/samueljaval/List-of-viruses-for-Open-Source-Anti-Virus/raw/master/viruses/all_viruses_compressed.json.zip"
req = requests.get(file_url)

zipped_file = zipfile.ZipFile(io.BytesIO(req.content))
unzipped_file = zipped_file.read('all_viruses_compressed.json')
# eval() evaluates string to dict and .decode decodes bytes object to string 
viruses_dict = eval(unzipped_file.decode('utf-8'))
'''

file_url = "https://github.com/samueljaval/List-of-viruses-for-Open-Source-Anti-Virus/raw/master/viruses/all_viruses_compressed.json.zip"
req = requests.get(file_url)

zipped_file = zipfile.ZipFile(io.BytesIO(req.content))
unzipped_file = zipped_file.read('all_viruses_compressed.json')
# eval() evaluates string to dict and .decode decodes bytes object to string
viruses_dict = eval(unzipped_file.decode('utf-8'))

def main_loop_v2():
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
                    result = multiprocess_check_v2(checkfornew, viruses_dict)
                    if result:
                        alert("virus", checkfornew)
                    else:
                        alert("not_virus", checkfornew)

            # if newest thing is a folder (hopefully an unzipped one)
            elif os.path.isdir(checkfornew):
                if checkfornew != newest:
                    files_to_scan = unpack_folder(checkfornew)
                    for each in files_to_scan:
                        result = multiprocess_check_v2(each, viruses_dict)
                        # if any is a virus, alert
                        if result:
                            alert("virus", checkfornew)
                    else:
                        alert("not_virus", checkfornew)

        if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
            newest = checkfornew
        size_folder = new_size_folder

def one_file_v2(filename):
    dialogs.checking_dialog()
    result = multiprocess_check_v2(filename, viruses_dict)
    if result == True:
        alert("virus", filename)
    else:
        alert("not_virus", filename)

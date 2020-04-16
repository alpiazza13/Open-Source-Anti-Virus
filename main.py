import time
from os_functions import alert, newest_file, size_downloads, intro
from is_virus import is_virus
from helpers import formating_viruses, get_hex_compressed

viruses = ["viruses/virus1.txt", "viruses/virus2.txt", "viruses/virus3.txt", "viruses/try.jpg"]

viruses_dict = formating_viruses(viruses)

def main():
    intro()
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
                        alert("virus")
                    else:
                        alert("not_virus")
        if not checkfornew.endswith('.crdownload') and not checkfornew.endswith('.download'):
            newest = checkfornew
        size_folder = new_size_folder

main()

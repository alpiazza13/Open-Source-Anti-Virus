import os
import glob
import time
from helpers import fit_to_unix
import dialogs
import webbrowser


# check that the path is correct up to Downloads
def secure_path(checkfornew):
    right_path = os.path.expanduser('~')+"/Downloads/"
    i = 0
    while i < len(right_path):
        if not(checkfornew[i] == right_path[i]):
            return False
        i+=1
    return True

def check_item(checkfornew,item):
    for char in checkfornew:
        if char == item:
            return False
    return True

def security(checkfornew):
    check1 = check_item(checkfornew,"/-")
    check2 = check_item(checkfornew,"~")
    check3 = check_item(checkfornew,"..")
    check4 = check_item(checkfornew,"*")
    check5 = secure_path(checkfornew)
    check6 = check_item(checkfornew,"$")
    check7 = check_item(checkfornew,":")
    if check1 and check2 and check3 and check4 and check5 and check6 and check7:
        return True
    else :
        return False


def remove(checkfornew):
    #security layer
    if security(checkfornew):
        # i don't know the inner workings of os.remove so i treated it
        # and secured it as if it was the "rm" unix command to be safe.
        # Even if it might not be necessary, it doesn't hurt
        os.remove(checkfornew)


def alert(status, checkfornew):
    if status == "virus":
        result = dialogs.virus_dialog()
        if result == ['button returned:Yes\n']:
            remove(checkfornew)
    else:
        dialogs.all_good_dialog()


# get name of most recent file in downloads
def newest_file():
    list_of_files = glob.glob(os.path.expanduser('~')+"/Downloads/*")
    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file

# get size of downloads directory
def size_downloads():
    return len(os.listdir(os.path.expanduser('~')+"/Downloads"))


def remove(checkfornew):
    os.system("rm -rf " + fit_to_unix(checkfornew))


def open_github():
    url = "https://github.com/samueljaval/List-of-viruses-for-Open-Source-Anti-Virus"
    webbrowser.open_new_tab(url)

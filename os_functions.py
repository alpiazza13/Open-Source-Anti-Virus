import os
import glob
import time
from helpers import fit_to_unix



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

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def alert(status, checkfornew):
    if status == "virus":
        result = os.popen(""" osascript -e 'display dialog "THIS IS PROBABLY A VIRUS! Do you want us to delete the file for you? " buttons {"Yes","No"} with title "VIRUS CHECK" with icon Stop'
        """).readlines()
        print(result)
        if result == ['button returned:Yes\n']:
            remove(checkfornew)
    else:
        os.system("""
                    osascript -e 'display dialog "You are all good, this is most likely not a virus" buttons {"OK"} with title "VIRUS CHECK" with icon Note'
        """)

def intro():
    os.system("""osascript -e 'display dialog "You just opened VIRUS DETECTION
    We will tell you whenver we think you donwloaded a virus
    No need to worry about this anymore" buttons {"OK"} with title "VIRUS DETECTION APP"
    '""")

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

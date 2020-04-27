import os
import pync

def intro():
    os.system("""osascript -e 'display dialog "Welcome to Virus Detection!

We will monitor everything that enters your downloads folder and notify you whenever we think you downloaded a virus.

You will see the app in you Menu Bar at the top of your screen with the label Anti-🦠.

YOU MUST CLICK START IN THE MENU BAR TO START THE APP!!!

With the Single File Check option, you can select any file from your computer and we will check whether it is a virus." buttons {"OK"} default button "OK" with title "VIRUS DETECTION APP"
    '""")

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def virus_dialog():
    result = os.popen(""" osascript -e 'display dialog "THIS IS PROBABLY A VIRUS! Do you want us to delete the file for you? " buttons {"Yes","No"} with title "VIRUS CHECK" with icon Stop'
    """).readlines()
    return result

def all_good_dialog():
    pync.notify("All good - this is most likely not a virus", title="Anti-Virus App")

def help_dialog():
    os.system("""osascript -e 'display dialog "Welcome to VIRUS DETECTION

We will monitor everything that enters your downloads folder and notify you whenever we think you downloaded a virus.

You will see the app in you Menu Bar at the top of your screen with the label Anti-🦠.

YOU MUST CLICK START IN THE MENU BAR TO START THE APP!!!

With the Single File Check option, you can select any file from your computer and we will check whether it is a virus.

{This app was created by Alex Piazza, Kevin Koech, Samuel Javal and Jeremy Kattan in April 2020}" buttons {"OK"} default button "OK" with title "Anti-Virus App - Help/About"
'""")

def start_dialog():
    pync.notify("App successfully started - virus detection is now running.", title="Anti-Virus App")

def already_started():
    pync.notify("App already running, it's pointless to start it again ", title="Anti-Virus App")

def pause_dialog():
    pync.notify("App paused", title="Anti-Virus App")

def wrong_pause():
    pync.notify("App is not currently running, so why would you pause it?", title="Anti-Virus App")

def cloning_dialog():
    pync.notify("Warning: There was a problem accessing the data we need to check for viruses, please check your internet connection", title="Anti-Virus App")

def file_dialog():
    result = os.popen("""osascript -e 'choose file' """).readlines()
    if result != []:
        os.chdir(os.path.expanduser('~'))
        os.system("cd ../..")
        filename = ""
        for x in result[0][18:-1]:
            if x == ":":
                filename += "/"
            else :
                filename += x
    return filename

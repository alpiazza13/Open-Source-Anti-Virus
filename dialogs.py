import os
import pync

def intro():
    os.system("""osascript -e 'display dialog "You just opened VIRUS DETECTION
We will tell you whenver we think you donwloaded a virus
No need to worry about this anymore

You will see the app in you Menu Bar at the top of your screen.
Click Start in the Menu Bar to start the app.
With the Single File Check option, you can check if a file you already have on your computer is a virus or not." buttons {"OK"} default button "OK" with title "VIRUS DETECTION APP"
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
    pync.notify("You are all good, this is most likely not a virus", title="Anti-Virus App")

def help_dialog():
    os.system("""osascript -e 'display dialog "{This app was created by Alex Piazza, Kevin Koech, Samuel Javal and Jeremy Kattan in April 2020}" buttons {"OK"} default button "OK" with title "Anti-Virus App - Help/About"
'""")

def start_dialog():
    pync.notify("You successfully started the app. It is now running.", title="Anti-Virus App")

def already_started():
    pync.notify("Warning: You already started the app, you cannot start it again.", title="Anti-Virus App")

def pause_dialog():
    pync.notify("You successfully paused the app.", title="Anti-Virus App")

def wrong_pause():
    pync.notify("Warning: You have not started the app, you cannot pause it.", title="Anti-Virus App")

def cloning_dialog():
    pync.notify("Warning: We had a problem downloading our test viruses, please check your internet connection", title="Anti-Virus App")

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

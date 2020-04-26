import os
import shutil
from dialogs import clonning_dialog


def get_viruses_github():
    try :
        shutil.rmtree("List-of-viruses-for-Open-Source-Anti-Virus")
    except FileNotFoundError:
        pass

    os.system("git clone https://github.com/samueljaval/List-of-viruses-for-Open-Source-Anti-Virus.git")

    try :
        mypath = "List-of-viruses-for-Open-Source-Anti-Virus/viruses"
        #only returns the files
        virus_list = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    except FileNotFoundError:
        clonning_dialog()

    new_list = []
    for virus in virus_list:
        new_list.append("List-of-viruses-for-Open-Source-Anti-Virus/viruses/" + virus)

    virus_list = new_list

    return virus_list

from loop_and_onefile import viruses_dict
from is_virus import is_virus, is_virus_v2
from helpers import get_hex_compressed, unpack_folder
print("done getting json! \n")



from os import listdir
from os.path import isfile, join

viruses = [virus for virus in listdir("testfiles/viruses") if virus != ".DS_Store"]
not_viruses = [not_virus for not_virus in listdir("testfiles/non_viruses") if not_virus != ".DS_Store"]


# print("ORIGINAL METHOD \n")
# print("Virus checking results (hopefully all True):")
# for virus in viruses:
#     bool = is_virus(get_hex_compressed("testfiles/viruses/"+virus), viruses_dict, 200)
#     print(virus + ": ", bool)
# print("\n")
#
#
# print("Non-virus checking results (hopefully all False):")
# for not_virus in not_viruses:
#     bool = is_virus(get_hex_compressed("testfiles/non_viruses/"+not_virus), viruses_dict, 200)
#     print(not_virus + ": ", bool)
# print("\n")


# uncomment to try kevin's method, but not sure if it works
print("KEVINS METHOD")
print("Virus checking results (hopefully all True):")
for virus in viruses:
    bool = is_virus_v2("testfiles/viruses/"+virus, viruses_dict)
    print(virus + ": ", bool)
print("\n")

print("Non-virus checking results (hopefully all False):")
for not_virus in not_viruses:
    bool = is_virus_v2("testfiles/non_viruses/"+not_virus, viruses_dict)
    print(not_virus + ": ", bool)
print("\n")

import binascii
filename = 'dan_hw.py'
with open(filename, 'rb') as f:
    content = f.read()
hex1 = binascii.hexlify(content)
# get rid of first 2 and last 1 characters
str_hex = str(hex1)[2:-1]
print(type(str_hex))
print(len(str_hex))
print(str_hex[-2])
# print(str_hex)
# candidates for number: 500, 1000

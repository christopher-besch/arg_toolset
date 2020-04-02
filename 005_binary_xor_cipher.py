# convert binary to ascii text
import math

# get cipher from file if available
file_location = input("file location: ")

if file_location == '':
    cipher = input("paste the cipher here: ")
else:
    with open(file_location, encoding='utf-8') as file:
        cipher = file.read()

# characters between each word
delimiter = input("delimiter: ")
# in which base is the cipher?
base = int(input("base: "))
# calculate length of every word
length = int(math.log(256, base))
print('length of each word: {}'.format(length))

# replace every line break with the delimiter
cipher = cipher.replace('\n', delimiter)

# when there is a delimiter
if delimiter != "":
    cipher = cipher.split(delimiter)
# if not
else:
    # cut cipher into list of words
    # only available if math.log(256, base) is a whole number (e.g. can't cut a slice with a length of 2.43)
    cipher = [cipher[i:i + length] for i in range(0, len(cipher), length)]

# going threw every XOR key (from 0 to 255)
for key in range(0, 256):
    # convert into characters
    text = ""
    for char in cipher:
        # perform XOR calculation
        decoded_char = int(char, base) ^ key

        text += chr(decoded_char)

    # replacing line breaks
    print("{}\t{}".format(key, text.replace('\n', '').replace('\r', '')))

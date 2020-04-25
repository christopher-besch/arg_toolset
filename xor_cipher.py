"""
convert ASCII encoded text from any base to a readable string and perform brute force XOR cipher decryption
"""

from math import log


def xor_options(word_list):
    # going through every XOR key (from 0 to 255)
    for key in range(0, 256):
        # convert into characters
        text = ""
        for word in word_list:
            # decode after XOR with current key
            text += chr(word ^ key)

        yield key, text


if __name__ == "__main__":
    # get cipher from file if unavailable
    cipher = input("paste the text here: ").upper()
    if cipher == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            cipher = file.read().upper()

    # characters between each word
    delimiter = input("delimiter: ")
    # replace every line break with the delimiter
    cipher = cipher.replace('\n', delimiter)

    # in which base is the cipher?
    base = int(input("base: "))

    # when there is a delimiter
    if delimiter != "":
        cipher = [int(entry, base) for entry in cipher.split(delimiter)]
    # if there is not character splitting one word from another
    else:
        # calculate length of every word
        # 256 = base ** length of each word
        # log base(256) = length
        # (256 since working with 8bit ASCII)
        length = int(log(256, base))
        print(f"length of each word: {length}")
        # cut cipher into list of words
        # only available if log(256, base) is a whole number (e.g. can't cut a slice with a length of 2.43)
        # and convert to base 10
        cipher = [int(cipher[i:i + length], base) for i in range(0, len(cipher), length)]

    for option in xor_options(cipher):
        # print option without line breaks for readability
        print(f"{option[0]}:\t{option[1]}".replace("\n", ""))

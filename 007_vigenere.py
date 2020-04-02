# encrypt with the vigenere cipher
char_list = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z'
]

# encrypt or decrypt?
encrypt = input("encrypt? (alternative is decryption) Y/n: ")
encrypt = encrypt == 'Y' or encrypt == 'y'
if encrypt:
    text = input("paste text here: ").upper()
else:
    text = input("paste cipher here: ").upper()
key = input("paste key here: ").upper()

# remove every unknown character in the key
key_list = []
for char in key:
    if char in char_list:
        key_list.append(char)
key = ''.join(key_list)

# going threw every character in the text
# key copied to the length of the length of the text
copied_key = ""
cipher = ""
# every letter that get's skipped will increase this variable
skipped_letters = 0
for idx, char in enumerate(text):
    # get current key char
    # don't skip key letters
    key_char_idx = idx - skipped_letters
    # rollover when the current index is higher than the length of the key
    while key_char_idx >= len(key):
        key_char_idx -= len(key)
    key_char = key[key_char_idx]

    if char in char_list:
        # adding when encrypting
        if encrypt:
            cipher_char_idx = char_list.index(char) + char_list.index(key_char)
            # rollover
            while cipher_char_idx >= len(char_list):
                cipher_char_idx -= len(char_list)
        # subtracting when decrypting (a negative rollover is not necessary)
        else:
            cipher_char_idx = char_list.index(char) - char_list.index(key_char)

        # add characters
        copied_key += key_char
        cipher += char_list[cipher_char_idx]
    # add the char itself if it isn't included in the char dict
    else:
        copied_key += char
        cipher += char
        # this letter has been skipped
        skipped_letters += 1

# print results
if encrypt:
    print()
    print("Plaintext:\t{}".format(text))
    print("Keyword:\t{}".format(copied_key))
    print("Ciphertext:\t{}".format(cipher))
else:
    print()
    print("Ciphertext:\t{}".format(text))
    print("Keyword:\t{}".format(copied_key))
    print("Plaintext:\t{}".format(cipher))

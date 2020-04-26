"""
encrypt/decrypt with the vigenere cipher
"""


# decrypt when encrypt == False, when this is the case the text and cipher variables aren't named correctly
def vigenere_crypt(text, key, encrypt=True, char_list=None):
    # replace char_list with default
    if char_list is None:
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

    # going through every character in the text
    copied_key = ""
    cipher = ""
    # every letter that get's skipped (e.g. blanks) will increase this variable -> key index doesn't rises with blanks
    skipped_letters = 0
    for idx, char in enumerate(text):
        # get current key char
        # don't skip key letters
        key_char_idx = idx - skipped_letters
        # rollover when the current index is higher than the length of the key
        while key_char_idx >= len(key):
            key_char_idx -= len(key)
        key_char = key[key_char_idx]

        # when the key is unknown at this position
        if key_char not in char_list:
            # add characters
            copied_key += key_char
            cipher += key_char

        elif char in char_list:
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
    return copied_key, cipher


if __name__ == "__main__":
    # get cipher from file if unavailable
    input_text = input("paste the text here: ").upper()
    if input_text == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            input_text = file.read().upper()
    vigenere_key = input("paste key here: ").upper()

    print()
    print(f"Original:  {input_text}")

    final_key, encrypted = vigenere_crypt(input_text, vigenere_key, encrypt=True)
    print(f"Final Key: {final_key}")
    print(f"Encrypted: {encrypted}")
    final_key, decrypted = vigenere_crypt(input_text, vigenere_key, encrypt=False)
    print(f"Decrypted: {decrypted}")

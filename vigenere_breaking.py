"""
decrypt a vigenere cipher with a known part of the decrypted text
"""

from vigenere import vigenere_crypt


# get amount of unknown characters in a string
def blanks_amount(phrase, char_list=None):
    # replace char_list with default
    if char_list is None:
        char_list = char_list_default
    # a blank is an unknown character
    blanks = 0
    for character in phrase:
        if character not in char_list:
            blanks += 1
    return blanks


# check if string can build key
def check_str(string, key, char_list=None):
    # replace char_list with default
    if char_list is None:
        char_list = char_list_default
    # True until an unfitting character is found
    match = True
    # going through every character in the key
    for key_idx, key_char in enumerate(key):
        # when the current key character is unknown, the string can fit -> match stays True
        if key_char in char_list:
            # get current string char
            str_idx = key_idx
            # rollover when the current key index is higher than the length of the string
            while str_idx >= len(string):
                str_idx -= len(string)

            # when the current string char is known and not equal to the current key char,
            # the string does not match with the key
            if string[str_idx] in char_list:
                if string[str_idx] != key_char:
                    match = False
                    break
            # when the current char is unknown, it will be overwritten by the current key char
            # for example: when this is the key
            # TESTTESTTESTTEST
            # and the string is
            # T_S_
            # then it is obvious that the first blank is supposed to be an E and the second one a T
            else:
                string[str_idx] = key_char
    return match


# return every key that could have been used
# text_partly is a part of the plain text that is already known
def get_key_options(cipher, text_partly, char_list=None, unknown_char="_"):
    # replace char_list with default
    if char_list is None:
        char_list = char_list_default
    if unknown_char in char_list:
        raise ValueError("the unknown char is not allowed to be in the character list!")

    # get list with indices of every character from the cipher not in char_list (=gaps in cipher)
    unknown_chars = []
    for idx, char in enumerate(cipher):
        if char not in char_list:
            unknown_chars.append(idx)

    # going through every possible position of the known part in the cipher and get every possible (extended) key
    # no overlap allowed
    strings_list = []
    for shift in range(0, len(cipher) - len(text_partly) + 1):
        # shift known part:
        # _________________text_partly__________________
        text_partly_shifted = unknown_char * shift
        text_partly_shifted += text_partly
        # add characters to the end so that len(cipher) == len(text_partly_shifted)
        text_partly_shifted += unknown_char * (len(cipher) - len(text_partly_shifted))

        # generate key_partly_list <- see which key could have created the cipher from the text (decrypting)
        key_partly_list = []
        # also terminate if the known part does not align with the cipher (gaps aligning)
        usable = True
        for idx, char in enumerate(text_partly_shifted):
            if char in char_list:
                # when there is a known character in the known text that is aligned with a gap
                if cipher[idx] not in char_list:
                    usable = False
                    break
                else:
                    # decrypt -> create key char
                    key_char_idx = char_list.index(cipher[idx]) - char_list.index(char)
                    key_partly_list.append(char_list[key_char_idx])
            # every unknown char in text_partly is either legit when aligned with the same char in the cipher
            # or an unknown part of the key
            # when the character is only a gap <- current index is in unknown_chars
            elif idx not in unknown_chars:
                # add unknown character to list
                key_partly_list.append(char)
        # get new key if this one is unusable
        if not usable:
            continue

        # trying to find a repeating string in key_partly_list
        # starting with length 1, going up to the length of the key
        # list with every repeating string
        strings_list_this = []
        # going through every possible length of the substring
        for len_rep_str in range(1, len(key_partly_list) + 1):
            # going through every complete string (no unknown characters) inside key_partly with
            for idx in range(0, len(key_partly_list), len_rep_str):
                # when the index would be out of range
                # when the current index plus the "shift" is at least the length of key_partly_list
                if idx + len_rep_str > len(key_partly_list):
                    break

                # cut string out of the key
                rep_str = key_partly_list[idx:idx + len_rep_str]

                # build list out of string
                rep_str_list = []
                # True when at least one known character found
                usable = False
                for rep_str_char in rep_str:
                    # convert any unknown characters into ' '
                    if rep_str_char in char_list:
                        rep_str_list.append(rep_str_char)
                        usable = True
                    else:
                        rep_str_list.append(" ")

                # only proceed when the string is usable <- there are known characters in the string
                if usable:
                    # check if string can build key that matches with key_partly_list
                    if check_str(rep_str_list, key_partly_list):
                        rep_str = ''.join(rep_str_list)
                        # only add a string that doesn't exit in the list yet
                        if rep_str not in strings_list_this:
                            strings_list_this.append(rep_str)
        # add found keys to others
        strings_list += strings_list_this

    # sort list by length, the longer the better
    strings_list.sort(key=lambda string: len(string))
    # delete doubles in list (e.g. "KEY" and "KEYKEY" are doubles)
    keys_list = []
    for key in strings_list:
        # False when this key is just a repeating copy of another one
        usable = True
        # going through every already checked key
        for done_key in keys_list:
            # when an already checked key is a part of the current key
            # and when key can be restlessly divided into parts with the length of the length of done_key
            if done_key in key and len(key) % len(done_key) == 0:
                # cut key into parts
                key_part_list = [key[i:i + len(done_key)] for i in range(0, len(key), len(done_key))]

                # False when this key is just a repeating copy of done_key
                this_way_usable = False
                # going through every part
                for part in key_part_list:
                    # when this part is somehow different from done_key
                    if part != done_key:
                        this_way_usable = True
                        break
                if not this_way_usable:
                    usable = False
                    break
        # when no test could prove that this key is just a copy
        if usable:
            keys_list.append(key)

    # sort list by amount of unknown characters, the fewer the better
    keys_list.sort(key=lambda string: blanks_amount(string, char_list=char_list), reverse=True)
    # sort list by length, the shorter the better
    keys_list.sort(key=lambda string: len(string), reverse=True)

    return keys_list


# get length of line over repeating part of the key
def get_len_line(text, repeating_key, char_list=None):
    # replace char_list with default
    if char_list is None:
        char_list = char_list_default
    len_line = 0
    str_idx = 0
    for char in text:
        # when the length of the key has been reached, the loop is over
        if str_idx >= len(repeating_key):
            break
        # when this character in the text is known, it will be underlined at the cost of one index
        if char in char_list:
            len_line += 1
            str_idx += 1
        # when this is an unknown character, it will be underlined "for free"
        else:
            len_line += 1
    return len_line


char_list_default = [
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

if __name__ == "__main__":
    # get cipher from file if unavailable
    input_text = input("paste the text here: ").upper()
    if input_text == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            input_text = file.read().upper()
    known_part = input("paste known parts of the text here (unknown parts should be marked with '_'): ").upper()

    for vigenere_key in get_key_options(input_text, known_part):
        final_key, decrypted = vigenere_crypt(input_text, vigenere_key, encrypt=False)
        print()
        print()
        print("key: {}".format(vigenere_key))
        print('_' * get_len_line(decrypted, vigenere_key))
        print(final_key)
        print(decrypted)

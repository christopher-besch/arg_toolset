# decrypt a cipher and parts of its key
# reconstruct the key from some known parts


# get amount of unknown characters in a string
def blanks_amount(phrase):
    # a blank is an unknown character
    blanks = 0
    for character in phrase:
        if character not in char_list:
            blanks += 1
    return blanks


# check if string can build key that matches with a partly key
def check_str(string, full_key_partly):
    # True until an unfitting character is found
    match = True
    # going threw every character in the kore or less full key
    for key_idx, key_char in enumerate(full_key_partly):
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
            else:
                string[str_idx] = key_char
    return match


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
unknown_char = "_"
if unknown_char in char_list:
    raise ValueError("the unknown char is not allowed to be in the character list!")


# get cipher from file if unavailable
cipher = input("paste the cipher here: ").upper()
if cipher == '':
    file_location = input("file location: ")
    with open(file_location, encoding='utf-8') as file:
        cipher = file.read().upper()


text_partly = input("paste known parts of the text here (unknown parts should be marked with '{}'): "
                    .format(unknown_char)).upper()

# get list with indices of every character from the cipher not in char_list (=gaps in cipher)
unknown_chars = []
for idx, char in enumerate(cipher):
    if char not in char_list:
        unknown_chars.append(idx)


# going threw every possible position of the known part in the cipher and get every possible key (already extended)
strings_list = []
for shift in range(0, len(cipher) - len(text_partly) + 1):
    # shift known part
    text_partly_shifted = unknown_char * shift
    # add known part to text_partly_shifted
    text_partly_shifted += text_partly
    # add characters to end so that len(cipher) == len(text_partly_shifted)
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
            # decrypt
            key_char_idx = char_list.index(cipher[idx]) - char_list.index(char)
            key_partly_list.append(char_list[key_char_idx])
        # every unknown char in key_partly is either legit when aligned with the same char in the cipher
        # or an unknown part of the key
        # when the character is only a gap <- current index is in unknown_chars
        elif idx not in unknown_chars:
            # add unknown character to list
            key_partly_list.append(char)
    # get new key if this one is unusable
    if not usable:
        continue

    # trying to find a repeating string in key_partly
    # starting with length 1, going up to the length of the key
    # list with every repeating string
    strings_list_this = []
    # going threw every possible length of the substring
    for len_rep_str in range(1, len(key_partly_list) + 1):
        # going threw every complete string (no unknown characters) inside key_partly with
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
                    rep_str_list.append(' ')

            # only proceed when the string is usable <- there are known characters in the string
            if usable:
                # check if string can build key that matches with key_partly
                if check_str(rep_str_list, key_partly_list):
                    rep_str = ''.join(rep_str_list)
                    # only add a string that doesn't exit in the list yet
                    if rep_str not in strings_list_this:
                        strings_list_this.append(rep_str)
    # add found keys to others
    strings_list += strings_list_this

# sort list by amount of unknown characters, the fewer the better
strings_list.sort(key=blanks_amount, reverse=True)
# sort list by length, the shorter the better
strings_list.sort(key=lambda string: len(string), reverse=True)

# delete doubles in list ("KEY" and "KEYKEY" are doubles)
keys_list = []
for key in strings_list:
    # False when this key is just a repeating copy of another one
    usable = True
    # going threw every already checked key
    for done_key in keys_list:
        # when an already checked key is a part of the current key
        # and when key can be restlessly divided into parts with the length of the length of done_key
        if done_key in key and len(key) % len(done_key) == 0:
            # cut key into parts
            key_part_list = [key[i:i + len(done_key)] for i in range(0, len(key), len(done_key))]

            # False when this key is just a repeating copy of done_key
            this_way_usable = False
            # going threw every part
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

# decrypt with every found key option (like in vigenere.py)
for key in keys_list:
    copied_key = ""
    text = ""
    # every letter that get's skipped will increase this variable
    skipped_letters = 0
    for idx, char in enumerate(cipher):
        # get current key char
        # don't skip key letters
        key_char_idx = idx - skipped_letters
        # when the current index is higher than the length of the key
        while key_char_idx >= len(key):
            key_char_idx -= len(key)

        key_char = key[key_char_idx]
        # when the current cipher char is known
        if char in char_list:
            # when the current key char is known
            if key_char in char_list:
                cipher_char_idx = char_list.index(char) - char_list.index(key_char)
                # rollover (a negative rollover is not necessary)
                while cipher_char_idx >= len(char_list):
                    cipher_char_idx -= len(char_list)

                copied_key += key_char
                text += char_list[cipher_char_idx]

            # when this part of the key is unknown, it will be underlined
            else:
                copied_key += key_char
                text += key_char
        # add the char itself if it isn't included in the char dict
        else:
            copied_key += char
            text += char
            skipped_letters += 1

    # line over repeating part of the key
    len_line = 0
    str_idx = 0
    for char in text:
        # when the length of the key has been reached, the loop is over
        if str_idx >= len(key):
            break
        # when this character in the text is known, it will be underlined at the cost of one index
        if char in char_list:
            len_line += 1
            str_idx += 1
        # when this is an unknown character, it will be underlined "for free"
        else:
            len_line += 1

    # print this option
    print()
    print()
    print("key: {}".format(key))
    print('_' * len_line)
    print(copied_key)
    print(text)

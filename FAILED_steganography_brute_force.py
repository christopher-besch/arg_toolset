"""
failed attempt of brute forcing steganography
failed so no effort of making it useful have been taken
DO NOT USE!!!
"""

import re


# recursive function to get every password option out of a list of characters
def get_options(chars, option_len):
    options = []
    for idx, char in enumerate(chars):
        # only when not already done
        already_used = False
        for option in options:
            if char == option[0]:
                already_used = True
                break
        if already_used:
            continue

        # end recursion when no more chars are requested
        if option_len == 1:
            options.append([char])
        elif option_len > 1:
            # get other options
            new_options = get_options(chars[idx + 1:], option_len - 1)
            for new_option in new_options:
                # this part of the option starts with char
                options.append([char] + new_option)

    return options


# import the list with every english word
with open("corncob_lowercase.txt", encoding='utf-8') as file:
    words = file.read().split('\n')

# get cipher from file if available
file_location = input("file location: ")
if file_location == '':
    cipher = input("paste the cipher here: ")
else:
    with open(file_location, encoding='utf-8') as file:
        cipher = file.read().lower()

# get every word
matches = re.findall(r'\b[a-z]+\b', cipher)
# get list with every starting character
starts = []
for match in matches:
    starts.append(match[0])

# calculate length of the longest word and fill words_dict
max_len = 0
# dictionary with every word sorted by length
words_dict = {}
for word in words:
    # create new entry or fll an existent one
    if len(word) in words_dict.keys():
        words_dict[len(word)].append(word)
    else:
        words_dict[len(word)] = [word]

    if len(word) > max_len:
        max_len = len(word)
# when there are fewer chars then max_len
if max_len > len(starts):
    max_len = len(starts)

# should start by one
# but can be higher if lower values have already been calculated
start_length = 8

# get every possible word
for length in range(start_length, max_len + 1):
    # only when there is an english word with this length
    if length in words_dict.keys():

        # get every found english word
        passwords = get_options(starts, length)
        final_passwords = []
        # going through every english word with this length
        for word in words_dict[length]:
            # convert string to list
            word_list = []
            for char in word:
                word_list.append(char)

            if word_list in passwords:
                final_passwords.append(word)
                print(word)

        with open("results/passwords_{}.txt".format(length), 'w') as file:
            file.write('\n'.join(final_passwords))

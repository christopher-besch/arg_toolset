"""
perform a brute force caesar cipher decryption
"""


# class for each possible shift
class Possibility:
    def __init__(self, string, shift):
        self.string = string
        self.shift = shift

    def __repr__(self):
        return self.string


# encrypt/decrypt caesar cypher/text
def caesar(string, char_list=None):
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

    # trying every value of n (=amount shifted by)
    possibilities = []
    for n in range(0, len(char_list)):

        final_text = ""
        for char in list(string):
            # only shift supported characters
            if char in char_list:
                # index of the new character the old one is replaced by
                index_shifted = char_list.index(char) + n
                # rollover (when the index is bigger than the length of the list)
                while index_shifted >= len(char_list):
                    index_shifted -= len(char_list)
                # append new char to new text
                final_text += char_list[index_shifted]

            # when the char is not known
            else:
                final_text += char
        # save this possibility
        possibilities.append(Possibility(final_text, n))

    return possibilities


if __name__ == "__main__":
    # get cipher from file if unavailable
    cipher = input("paste the text here: ").upper()
    if cipher == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            cipher = file.read().upper()

    for possibility in caesar(cipher):
        print("{}:\t{}".format(possibility.shift, possibility.string))

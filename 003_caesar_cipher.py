# encrypt/decrypt caesar cypher/text

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

text = input("paste the cipher here: ").upper()

# trying every value of n possible
for n in range(0, len(char_list)):
    final_text = ""
    for char in text:
        # only shift supported characters
        if char in char_list:
            index_shifted = char_list.index(char) + n

            # rollover
            while index_shifted >= len(char_list):
                index_shifted -= len(char_list)

            final_text += char_list[index_shifted]
        else:
            final_text += char
    print("{}\t{}".format(n, final_text))

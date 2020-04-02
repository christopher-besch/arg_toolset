# assign each char a letter

substitutes = {
    "1": 'A',
    "2": 'B',
    "3": 'C',
    "4": 'D',
    "5": 'E',
    "6": 'F',
    "7": 'G',
    "8": 'H',
    "9": 'I',
    "01": 'A',
    "02": 'B',
    "03": 'C',
    "04": 'D',
    "05": 'E',
    "06": 'F',
    "07": 'G',
    "08": 'H',
    "09": 'I',
    "10": 'J',
    "11": 'K',
    "12": 'L',
    "13": 'M',
    "14": 'N',
    "15": 'O',
    "16": 'P',
    "17": 'Q',
    "18": 'R',
    "19": 'S',
    "20": 'T',
    "21": 'U',
    "22": 'V',
    "23": 'W',
    "24": 'X',
    "25": 'Y',
    "26": 'Z'
}

inverse_substitutes = {v: k for k, v in substitutes.items()}

cipher = input("paste the cipher here: ").upper()

delimiter = input("delimiter: ")

# cut at delimiters if existent
if delimiter != '':
    cipher = cipher.split(delimiter)

text_list = []

for char in cipher:
    if char in substitutes.keys():
        text_list.append(substitutes[char])

    elif char in inverse_substitutes.keys():
        text_list.append(inverse_substitutes[char])

    else:
        text_list.append(char)

print(delimiter.join(text_list))

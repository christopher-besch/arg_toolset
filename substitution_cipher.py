"""
substitute every letter with it's number from the alphabet and the other way around
"""


# assign each char a letter
def substitute(string, substitutes=None, joint=''):
    # replace substitutes with default
    if substitutes is None:
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
    # create dictionary with substitutes in reversed order
    inverse_substitutes = {v: k for k, v in substitutes.items()}
    # update dict
    substitutes = dict(**substitutes, **inverse_substitutes)

    # cut at delimiters if existent
    if joint != '':
        string = string.split(joint)
    # or just convert to list
    else:
        string = list(string)

    # convert every char
    text_list = []
    current_idx = 0
    while current_idx < len(string):
        current_char = string[current_idx]
        # add the current char with the next one (e.g. "02" -> "B")
        # only when there is no delimiter and a next one exists
        if joint == '' and current_idx + 1 < len(string):
            double_char = current_char + string[current_idx + 1]
            if double_char in substitutes.keys():
                text_list.append(substitutes[double_char])
                # jump 2 indices <- next char already used
                current_idx += 2
                continue
        # or add only this char converted
        if current_char in substitutes.keys():
            text_list.append(substitutes[current_char])
            current_idx += 1
        # or itself if it can't be substituted
        else:
            text_list.append(current_char)
            current_idx += 1

    return joint.join(text_list)


if __name__ == "__main__":
    # get cipher from file if unavailable
    cipher = input("paste the text here: ").upper()
    if cipher == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            cipher = file.read().upper()

    delimiter = input("delimiter: ")

    print(substitute(cipher, joint=delimiter))

"""
return every upper case character from a text
"""


def only_upper(string):
    text = ""
    for char in string:
        if char.isupper():
            text += char
    return text


if __name__ == "__main__":
    # get cipher from file if unavailable
    cipher = input("paste the text here: ")
    if cipher == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            cipher = file.read()

    print(only_upper(cipher))

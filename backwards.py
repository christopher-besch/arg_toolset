"""
reverse a text
"""


def reverse(string):
    return string[::-1]


if __name__ == "__main__":
    # get cipher from file if unavailable
    cipher = input("paste the text here: ")
    if cipher == '':
        file_location = input("file location: ")
        with open(file_location, encoding='utf-8') as file:
            cipher = file.read()

    print(reverse(cipher))

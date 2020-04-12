# get cipher from file if available
file_location = input("file location: ")

if file_location == '':
    cipher = input("paste the cipher here: ")
else:
    with open(file_location, encoding='utf-8') as file:
        cipher = file.read()

text = ""
for char in cipher:
    if char.isupper():
        text += char

print(text)

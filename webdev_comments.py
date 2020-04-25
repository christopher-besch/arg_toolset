"""
print every comment found in a (sub) directory
"""

import os
import re


# recursive function to get every file in a directory and every sub-sub-sub-...-directory
def get_file_names(dir_name):
    # create a list of file and sub directories
    # names in the given directory
    file_list = os.listdir(dir_name)
    all_files = []
    # iterate over every entry
    for entry in file_list:
        # create full path
        full_path = os.path.join(dir_name, entry)
        # if entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files += get_file_names(full_path)
        # if not then save the file itself
        else:
            all_files.append(full_path)

    return all_files


def get_comments(directory):
    # comments go in here
    files = {}
    # going through every file
    for file_location in get_file_names(directory):
        # read file
        try:
            with open(file_location, "r", encoding='utf-8') as file:
                text = file.read().split("\n")
        # when the file cannot be decoded <- image file
        except UnicodeDecodeError:
            continue

        # dict with every comment type
        files[file_location] = {}

        # searching for comments of every type
        for comment_type in comment_types:
            # add dict with line: comments
            files[file_location][comment_type.name] = {}

            # True when a comment starts but doesn't end
            hit = False
            # going through every line
            for idx, line in enumerate(text):
                # extract comments from line
                comments, hit = get_comments_line(line, comment_type.start_tag, comment_type.end_tag, is_comment=hit)

                # when there are comments
                if len(comments) > 0:
                    # add those to the dict for this type
                    files[file_location][comment_type.name][idx + 1] = comments

        # delete useless entries
        delete = True
        for comment_type in comment_types:
            # when there is a single type with comments, the dict won't be deleted
            if len(files[file_location][comment_type.name].keys()) > 0:
                delete = False
                break
        # only delete when necessary
        if delete:
            del files[file_location]
    return files


# recursive function to get every comment with start and ending part in a line
# is_comment is True when a comment started in the last line but didn't ended
# returning list_with_comments, new_is_comment
def get_comments_line(string, comment_start, comment_end, is_comment=False):
    # when there is a start tag or there was a start tag without an ending tag in the last line
    if re.search(comment_start, string) or is_comment:
        # starting from the beginning or the first start tag
        if is_comment:
            from_start = string
        else:
            # cutting at every start of comment and removing tag before comment
            start_cut = re.split(comment_start, string)
            from_start = ''.join(start_cut[2:])

        # when comment_end is None, the ending will be the line break
        if not comment_end:
            # if this is an empty comment, it will be removed
            if from_start == '':
                return [], False
            else:
                return [from_start.strip()], False
        # searching for ending
        elif re.search(comment_end, string):
            # cut at end of comment
            end_cut = re.split(comment_end, from_start)
            # list with first comment as first entry
            comment = [''.join(end_cut[:1]).strip()]

            # if this is an empty comment, it will be removed
            if comment[0] == '':
                comment = []

            # stuff after the comment
            rest = ''.join(end_cut[2:])
            # add every other comment in this line
            # line_break is True when there is a start but no end tag
            new_comments, line_break = get_comments_line(rest, comment_start, comment_end)
            comment += new_comments
            return comment, line_break
        else:
            # if this is an empty comment, it will be removed
            if from_start == '':
                return [], True
            else:
                return [from_start.strip()], True
    else:
        return [], False


# class for different comment types
class CommentType:
    def __init__(self, name, start_tag, end_tag=None):
        # names must be unique
        self.name = name
        self.start_tag = start_tag
        # when there is no end tag it goes until a line break
        self.end_tag = end_tag


if __name__ == "__main__":
    # dictionary with every type of comment
    comment_types = [
        CommentType("html",
                    re.compile(r'(<!--)'),
                    re.compile(r'(-->)')),
        CommentType("css/js",
                    re.compile(r'(/\*)'),
                    re.compile(r'(\*/)')),
        CommentType("js",
                    re.compile(r'(//)'))
    ]
    folder = input("path to directory: ")

    # printing results
    for loc, types in get_comments(folder).items():
        print()
        print(loc)

        for type_ in types:
            # only print the name if there is stuff inside
            if len(types[type_].keys()) > 0:
                print(type_)

                for line_num in types[type_]:
                    print("{}\t\t{}".format(line_num, "\n\t\t\t".join(types[type_][line_num])))

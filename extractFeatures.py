"""
Filename : extractFeatures
Author : Archit
Date Created : 3/19/2024
Description : 
Language : python3
"""
import json
import os


def extractFeatures(data):
    # Get the paths key from the json file
    paths = data['paths']
    # If the path doesnt exists return None
    if not paths:
        return False
    # Iterate over the paths and check if it has a get, post keys nested inside
    for path in paths:
        if 'get' in paths[path] or 'post' in paths[path]:
            return True
    return False


# def do_that_thing():
#     folder_path = 'APIsGuru'
#     valid_file_name = 'valid_APIs.txt'
#     with open(valid_file_name, 'w') as valid_file:
#         valid_file.truncate(0)
#
#     count = 0
#     # Iterate through all the files in APIsGuru folder
#     for file in os.listdir(folder_path):
#         count += 1
#         file_name = "APIsGuru/" + file
#
#         with open(file_name, 'r', encoding='utf-8') as api_file:
#             data = json.load(api_file)
#             valid = extractFeatures(data)
#             # If valid is True append the file name to the valid_APIs.txt
#             if valid:
#                 with open('valid_APIs.txt', 'a') as valid_file:
#                     valid_file.write(file + '\n')
#             else:
#                 print("Invalid API: ", file)
#     print("Processed: ", count)

def do_the_thing():
    valid_file_name = 'valid_APIs.txt'
    # Clear the file
    with open(valid_file_name, 'w') as valid_file:
        valid_file.truncate(0)

    invalid_file_count = 0

    count = 0
    folder_path = 'APIsGuru'
    # Iterate through all the files in APIsGuru folder
    for file in os.listdir(folder_path):
        if 'json' in file:
            count += 1
            file_name = "APIsGuru/" + file

            with open(file_name, 'r', encoding='utf-8') as api_file:
                data = json.load(api_file)
                valid = extractFeatures(data)
                # If valid is True append the file name to the valid_APIs.txt

                if valid:
                    with open(valid_file_name, 'a') as valid_file:
                        valid_file.write(file + '\n')
                else:
                    invalid_file_count += 1
                    # print("Invalid API: ", file)
    print("Invalid file count: ", invalid_file_count)
    print("Processed: ", count)


def main():
    do_the_thing()


if __name__ == "__main__":
    main()

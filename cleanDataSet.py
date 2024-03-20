"""
Filename : cleanDataSet
Author : Archit
Date Created : 3/19/2024
Description : 
Language : python3
"""
import os
import json
from extractFeatures import extractFeatures
from getServer import get_server
from checkNumPaths import get_num_paths


def do_the_thing():
    valid_file_name = 'final_valid_APIs_apisguru.txt'
    # Clear the file
    with open(valid_file_name, 'w') as valid_file:
        valid_file.truncate(0)

    invalid_file_count = 0

    folder_path = 'APIsGuru'
    # Iterate through all the files in APIsGuru folder
    for file in os.listdir(folder_path):
        if 'json' in file:
            file_name = "APIsGuru/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = json.load(api_file)
                    if extractFeatures(data) and get_server(data) and get_num_paths(data):
                        with open(valid_file_name, 'a') as valid_file:
                            valid_file.write(file + '\n')

                    else:
                        invalid_file_count += 1
            except json.JSONDecodeError:
                print(f"Error loading JSON from file: {file}. Skipping.")
                invalid_file_count += 1
                continue

    print("Invalid file count: ", invalid_file_count)


if __name__ == '__main__':
    do_the_thing()

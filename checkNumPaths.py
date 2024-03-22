"""
Check the number of paths in the API description
"""

import json
import os


def get_num_paths(data):
    try:
        if 'paths' in data.keys():
            if len(data['paths']) > 2:
                return True
    except KeyError as e:
        print("Error in get_num_paths")
        return False


def do_the_thing():
    valid_file_name = 'valid_num_paths_APIs_internet.txt'
    # Clear the file
    with open(valid_file_name, 'w') as valid_file:
        valid_file.truncate(0)

    invalid_file_count = 0
    total_json_count = 0

    folder_path = 'internet'
    # Iterate through all the files in APIsGuru folder
    for file in os.listdir(folder_path):
        # print(file)
        if 'json' in file:
            total_json_count += 1
            file_name = "internet/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = json.load(api_file)
                    valid = get_num_paths(data)
                    # If valid is True append the file name to the valid_APIs.txt
                    if valid:
                        with open(valid_file_name, 'a') as valid_file:
                            valid_file.write(file + '\n')
                    else:
                        invalid_file_count += 1
            except json.JSONDecodeError:
                print(f"Error loading JSON from file: {file}. Skipping.")
                invalid_file_count += 1
                continue
    print("Invalid file count: ", invalid_file_count)
    print("Total JSON file count: ", total_json_count)


def main():
    do_the_thing()


if __name__ == '__main__':
    main()

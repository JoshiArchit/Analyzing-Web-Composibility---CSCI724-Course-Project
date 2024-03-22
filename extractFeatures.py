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
    try:
        if 'paths' in data.keys():
            paths = data['paths']
            for path in paths:
                if 'get' in paths[path] or 'post' in paths[path]:
                    return True
    except KeyError as e:
        print("Error in extractFeatures")
        return False




def do_the_thing():
    valid_file_name = 'valid_extract_features_APIs_internet.txt'
    # Clear the file
    with open(valid_file_name, 'w') as valid_file:
        valid_file.truncate(0)

    invalid_file_count = 0
    total_json_count = 0

    folder_path = 'internet'
    # Iterate through all the files in APIsGuru folder
    for file in os.listdir(folder_path):
        if 'json' in file:
            total_json_count += 1
            file_name = "internet/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = json.load(api_file)
                    valid = extractFeatures(data)
                    # If valid is True append the file name to the valid_APIs.txt

                    if valid:
                        with open(valid_file_name, 'a') as valid_file:
                            valid_file.write(file + '\n')
                    else:
                        invalid_file_count += 1
            except FileNotFoundError as e:
                print(f"Error loading JSON from file: {file}. Skipping.")
                invalid_file_count += 1
                continue

    print("Invalid file count: ", invalid_file_count)
    print("Total JSON file count: ", total_json_count)


def main():
    do_the_thing()


if __name__ == "__main__":
    main()

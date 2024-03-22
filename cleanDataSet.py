"""
Filename : cleanDataSet
Author : Archit Joshi (aj6082), Athina Stewart (as1896)
Date Created : 3/19/2024
Description : Scan through data and remove any invalid files. The helper functions each satisfy the
basic constraints mentioned by the original authors.
Link to the original paper: https://ieeexplore.ieee.org/document/9885779
Language : python3
"""
import os
import json

import yaml


def extractFeatures(data):
    """
    Authors note - APIs need to have at least one endpoint with a description of schema of consumed
    or produced data. To satisfy this condition we scan through the data and check if there is a
    'get' or 'post' request in the paths.

    :param data: JSON data of the API
    :return: True if the API has at least one 'get' or 'post' request in the paths
    """
    try:
        if 'paths' in data.keys():
            paths = data['paths']
            for path in paths:
                if 'get' in paths[path] or 'post' in paths[path]:
                    return True
    except KeyError as e:
        print("Error in extractFeatures")
        return False


def get_num_paths(data):
    """
    Authors note - APIs need to have at least 3 paths three paths in order not to bias the
    average composability rate. To satisfy this condition we scan through the data and check if
    there are at least 3 paths in the API description.

    :param data: JSON data of the API
    :return: True if the API has at least 3 paths
    """
    try:
        if 'paths' in data.keys():
            if len(data['paths']) > 2:
                return True
    except KeyError as e:
        print("Error in get_num_paths")
        return False


def get_server(data):
    """
    Authors note - APIs need to have at least one realistic server (OAS v3) and base path (Swagger)
    URL. To satisfy this condition we scan through the data and check if there is a 'host' or
    'servers' key in the data.

    :param data: JSON data of the API
    :return: True if the API has a 'host' or 'servers' key
    """
    try:
        if 'swagger' in data.keys():
            if data['host']:
                return True
        else:
            if 'servers' in data.keys():
                for server in data['servers']:
                    if 'url' in server.keys() and server['url'] != '':
                        return True
    except KeyError as e:
        print("Error in get_server")
        return False


def clean_Data_Set():
    """
    Driver function to clean data adhering to the constraints mentioned by the authors in the
    original paper.

    :return: None
    """
    valid_file_name = 'final_valid_APIs_apisguru.txt'
    # Clear the file
    with open(valid_file_name, 'w') as valid_file:
        valid_file.truncate(0)

    invalid_file_count = 0
    valid_files = 0

    folder_path = 'APIsGuru'
    # Iterate through all the files in APIsGuru folder
    for file in os.listdir(folder_path):
        # Parse and process JSON files
        if 'json' in file:
            file_name = "APIsGuru/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = json.load(api_file)
                    if extractFeatures(data) and get_server(data) and get_num_paths(data):
                        with open(valid_file_name, 'a') as valid_file:
                            valid_file.write(file + '\n')
                        valid_files += 1
                    else:
                        invalid_file_count += 1
            except json.JSONDecodeError:
                print(f"Error loading JSON from file: {file}. Skipping.")
                invalid_file_count += 1
                continue

        # Parse and process YAML files
        elif 'yaml' in file:
            file_name = "internet/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = yaml.safe_load(api_file)
                    if get_num_paths(data) and extractFeatures(data) and get_server(data):
                        with open(valid_file_name, 'a') as valid_file:
                            valid_file.write(file + '\n')
                        valid_files += 1
                    else:
                        invalid_file_count += 1
            except yaml.YAMLError:
                print(f"Error loading YAML from file: {file}. Skipping.")
                continue

    print("Invalid file count: ", invalid_file_count)
    print("Valid file count: ", valid_files)


if __name__ == '__main__':
    clean_Data_Set()

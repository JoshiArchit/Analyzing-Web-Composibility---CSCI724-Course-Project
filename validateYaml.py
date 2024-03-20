"""
Filename : parseYaml
Author : Archit
Date Created : 3/20/2024
Description : File to parse the yaml file and extract the required information.
Language : python3
"""
# Need atleast 3 paths to be present in the yaml file
# Need to have atleast 1 get or post request in the paths
# Need to have atleast host or servers in the yaml file

import os
import yaml


def check_num_paths(data):
    try:
        if 'paths' in data.keys():
            paths = data['paths']
            if len(paths) >= 3:
                return True
    except:
        print("Error in check_num_paths")
        return False

    return False


def check_path_parameters(data):
    try:
        if 'paths' in data.keys():
            paths = data['paths']
            for path in paths:
                if 'get' in paths[path] or 'post' in paths[path]:
                    return True
    except:
        print("Error in check_path_parameters")
        return False
    return False


def check_server(data):
    try:
        if 'swagger' in data.keys():
            if data['host']:
                return True
        else:
            if 'servers' in data.keys():
                for server in data['servers']:
                    if 'url' in server.keys() and server['url'] != '':
                        return True
    except Exception as e:
        print("Error in check_server", e)
        return False
    return False


def read_yaml():
    valid_yaml = 'valid_yaml_APIs_internet.txt'

    # Clear the file
    with open(valid_yaml, 'w') as valid_file:
        valid_file.truncate(0)

    total_files = 0
    valid_files = 0
    invalid_files = 0

    folder_path = 'internet'
    for file in os.listdir(folder_path):
        if 'yaml' in file:
            file_name = "internet/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = yaml.safe_load(api_file)
                    if check_num_paths(data) and check_path_parameters(data) and check_server(data):
                        valid_files += 1
                    else:
                        invalid_files += 1
            except yaml.YAMLError:
                print(f"Error loading YAML from file: {file}. Skipping.")
                continue
            total_files += 1
    print("Valid files: ", valid_files)
    print("Invalid files: ", invalid_files)
    print("Total files: ", total_files)


def unit_test():
    """Test a single file"""
    filename = "internet/0a0fd644528edf05765d31eb49a272a1fbc4cf1b9f18713632151578c2f110ad.yaml"
    with open(filename, 'r', encoding='utf-8') as api_file:
        data = yaml.safe_load(api_file)
        valid_paths = check_num_paths(data)
        valid_parameters = check_path_parameters(data)
        valid_server = check_server(data)
        if valid_paths and valid_parameters and valid_server:
            print("Valid yaml file")


read_yaml()

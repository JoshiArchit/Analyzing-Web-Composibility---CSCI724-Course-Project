"""
Filename : extractMethodParameters
Author : Archit
Date Created : 3/20/2024
Description : Script to extract the get/post parameters from the API file.
Language : python3
"""
import json
import os


def getParameters(method_type, operation_number):
    doc = dict()
    if 'parameters' in method_type['get']:
        # Move to another method later
        doc['method'] = 'get'
        parameters = method_type['get']['parameters']
        for parameter in parameters:
            # Check if schema key exists. Then it's a complex object
            if 'schema' in parameter:
                schema = parameter['schema']
                doc['parameters'] = {
                    "name": parameter['name'],
                    "in": parameter['in'],
                    "description": parameter['description'],
                    "type": schema['type'],
                    "default": schema['default'],
                    "example": schema['example'],
                    "schema": parameter['schema']
                }
            else:
                doc['parameters'] = {
                    "name": parameter['name'],
                    "in": parameter['in'],
                    "description": parameter['description'],
                    "required": parameter['required'],
                    "type": parameter['type']
                }
    return doc


def extractParameters(api_file):
    doc = dict()
    # Document format ->
    # { "operation_0": {
    #       "method": "get",
    #       "parameters": {
    #           "name": "string",
    #           "in": "query",
    #           "description": "string",
    #           "required": "boolean",
    #           "type": "string"
    #       }
    #   }
    # }

    path_list = api_file['paths']
    operation_number = 0
    for path in path_list:
        # Get method type from each path
        method_type = path_list[path]
        if 'get' in method_type:
            doc[f"operation_{operation_number}"] = getParameters(method_type, operation_number)
            operation_number += 1
    return doc


def do_the_thing():
    document_list = []

    total_json_count = 0

    folder_path = 'APIsGuru'
    # Iterate through all the files in APIsGuru folder
    for file in os.listdir(folder_path):
        if 'json' in file:
            total_json_count += 1
            file_name = "APIsGuru/" + file
            try:
                with open(file_name, 'r', encoding='utf-8') as api_file:
                    data = json.load(api_file)
                    document = extractParameters(data)
                    document_list.append(document)
            except:
                raise FileNotFoundError("API file doesnt exist")


def unit_test():
    """Test for single API file to fix bugs and tune code"""
    file = 'APIsGuru/openapi.json.1'
    with open(file, 'r', encoding='utf-8') as api_file:
        data = json.load(api_file)
        document = extractParameters(data)
        print(document)


unit_test()

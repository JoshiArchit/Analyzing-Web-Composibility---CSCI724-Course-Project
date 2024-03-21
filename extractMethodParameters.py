"""
Filename : extractMethodParameters
Author : Archit ... but more like ** Athina **  :)
Date Created : 3/20/2024
Description : Script to extract the get/post parameters from the API file.
Language : python3
"""
import json
import os
from database import get_collection, post_collection


def getParameters(method_type, type):
    doc = dict()
    if 'parameters' in method_type[type]:
        # Move to another method later
        doc['method'] = type
        parameters = method_type[type]['parameters']
        for parameter in parameters:
            # Check if 'schema' key exists in parameter
            if 'schema' in parameter:
                schema = parameter['schema']
                doc['parameters'] = {
                    "name": parameter.get('name'),
                    "in": parameter.get('in'),
                    "description": parameter.get('description'),
                    "type": schema.get('type'),
                    "default": schema.get('default'),
                    "example": schema.get('example'),
                    "schema": parameter.get('schema')
                }
            else:
                # Check if keys exist in parameter dictionary
                doc['parameters'] = {
                    "name": parameter.get('name'),
                    "in": parameter.get('in'),
                    "description": parameter.get('description'),
                    "required": parameter.get('required'),
                    "type": parameter.get('type')
                }
    return doc

def extractParameters(api_file, type):
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
        if type in method_type:
            doc[f"operation_{operation_number}"] = getParameters(method_type, type)
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

    get_collection.delete_many({})
    post_collection.delete_many({})

    get_file = 'APIsGuru/openapi.json.1'
    post_file = 'APIsGuru/openapi.json.2'
    with open(get_file, 'r', encoding='utf-8') as api_file:
        get_data = json.load(api_file)
        get_document = extractParameters(get_data, 'get')
        get_collection.insert_one(get_document)
        get_document.pop('_id', None)

        print('\n')

    with open(post_file, 'r', encoding='utf-8') as api_file:
        post_data = json.load(api_file)
        post_document = extractParameters(post_data, 'post')
        post_collection.insert_one(post_document)
        post_document.pop('_id', None)

    # for operation_key, get_operation in get_document.items():
    #     print(f"Comparing operation: {operation_key}")
    #     get_parameters = get_operation.get('parameters', {})
    #     # Count matches for each GET parameter with POST parameters
    #     match_count = 0
    #     for post_operation in post_document.values():
    #         post_parameters = post_operation.get('parameters', {})
    #         for get_param_key, get_param_value in get_parameters.items():
    #             if get_param_value is not None:
    #                 post_param_value = post_parameters.get(get_param_key)
    #                 if post_param_value is not None and get_param_value == post_param_value:
    #                     match_count += 1
    #     print(f"Match count for operation {operation_key}: {match_count}")
    #     print('\n')

    """
    Steps
    1. iterates through the items in the post_document collection (this is the post parameter)
    2. iterates through each parameter in the post_operation
    3. iterates through the get_document collection (this is the get parameter)
    4. iterates through each parameter in the get_operation
    5. compares the get and post parameters values
    6. counts the number of matches
    """

    for post in post_collection.find({}):
        post.pop('_id', None)
        for post_operation_key, post_operation in post.items():
            print(f"Comparing operation: {post_operation_key}")
            post_parameters = post_operation.get('parameters', {})
            # Count matches for each POST parameter with GET parameters
            match_count = 0
            # for get_operation in get_document.values():
            for get_operation in get_collection.find({}):
                get_operation.pop('_id', None)
                for _, operation_data in get_operation.items():
                    # Access the 'parameters' key for each operation
                    get_parameters = operation_data.get('parameters', {})
                    # Compare GET and POST parameters
                    for post_param_key, post_param_value in post_parameters.items():
                        if post_param_value is not None:
                            get_param_value = get_parameters.get(post_param_key)
                            if get_param_value is not None and post_param_value == get_param_value:
                                match_count += 1
            print(f"Match count for operation {post_operation_key}: {match_count}")
            print('\n')



unit_test()
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


def getParameters(path_dictionary, method_type):
    doc = dict()
    doc['method'] = method_type
    doc['description'] = path_dictionary[method_type]['description']
    if 'parameters' in path_dictionary[method_type]:
        # Move to another method later
        parameters = path_dictionary[method_type]['parameters']
        for parameter in parameters:
            try:
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
                        "schema": parameter.get('schema'),
                        "response": parameter.get('responses')
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
            except KeyError as e:
                # print missing key
                print(f"KeyError: {e}")
                # Skip the parameter and continue
                continue
    return doc


def postParameters(api, path_dictionary, method_type):
    # Input is the path dictionary and the method type
    doc = dict()
    doc['description'] = path_dictionary['description']

    # Post request can send parameters via url or a request body, extract both
    if 'requestBody' in path_dictionary:
        # Extract parameters from the requestBody
        request_body = path_dictionary['requestBody']
        # Check if 'content' key exists in requestBody
        if not 'content' in request_body:
            # The parameters is stored as $ref, extract the reference
            ref = request_body['$ref']
            # Traverse the reference to get the parameters
            ref = ref.split('/')
            ref = ref[-1]
            try:
                # Get the parameters from the reference
                parameters = api['components']['schemas'][ref]
                # Extract the parameters
                doc['parameters'] = parameters['properties']
            except KeyError as e:
                # print missing key
                print(f"KeyError: {e}")
                # Skip the parameter and continue
                pass
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
        print("Operation number: ", operation_number)
        method_type = path_list[path]
        if 'get' in method_type:
            doc[f"operation_{operation_number}"] = getParameters(method_type, 'get')
        elif 'post' in method_type:
            doc[f"operation_{operation_number}"] = postParameters(api_file, method_type['post'], 'post')
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
        # get_document = extractParameters(get_data, 'get')
        get_document = extractParameters(get_data)
        get_collection.insert_one(get_document)
        get_document.pop('_id', None)

        print('\n')

    with open(post_file, 'r', encoding='utf-8') as api_file:
        post_data = json.load(api_file)
        # post_document = extractParameters(post_data, 'post')
        post_document = extractParameters(post_data)
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


def unit_test_post_document():
    post_file = 'APIsGuru/openapi.json.2'
    with open(post_file, 'r', encoding='utf-8') as api_file:
        post_data = json.load(api_file)
        post_document = extractParameters(post_data)
        print(post_document)


# unit_test()
unit_test_post_document()

"""
Filename : extractMethodParameters
Author : Archit Joshi (aj6082)
Date Created : 3/20/2024
Description : Script to extract the get/post parameters from the API file adhering to the
constraints listed by the authors in the original paper.
Link to the original paper: https://ieeexplore.ieee.org/document/9885779
Language : python3
"""
import json
import os
from database import get_collection, post_collection


def getParameters(api, path_dictionary):
    """
    Extracts the parameters from the API file for the get request. exclude_keys_list contains the
    keys that are not to be extracted as per the authors are they introduce inconsistencies in
    the data.

    :param api: openapi/swagger api specification file.
    :param path_dictionary: contents of the path attribute in the api file.
    :return: dictionary with parameters for the get request.
    """
    doc = dict()
    if 'parameters' in path_dictionary['get']:
        list_of_parameters = path_dictionary['get']['parameters']

        # List of keys that are not to be extracted
        exclude_keys_list = [
            "description", "title", "default", "example", "readOnly", "writeOnly", "example",
            "title", "enum", "required", "minimum", "maximum", "multipleOf", "minItems", "maxItems"
        ]

        # Iterate through the list of parameters
        for i, parameter in enumerate(list_of_parameters):
            operation = dict()
            if '$ref' in parameter:
                # Its a complexType with value stored as $ref, extract the reference
                ref = parameter['$ref']
                # Access dictionary using value of ref
                ref = ref.split('/')
                ref = ref[-1]

                # Extract the parameters from the reference
                try:
                    parameters = api['components']['parameters'][ref]
                    # Extract the values for the keys in the parameters except the keys in the
                    # exclude_keys_list
                    try:
                        for key, value in parameters.items():
                            if key not in exclude_keys_list:
                                if key == 'schema':
                                    value = api['components']['parameters'][ref]['schema']['type']
                                    operation['type'] = value
                                else:
                                    operation[key] = value
                    except KeyError as e:
                        # Skip the parameter and continue
                        continue
                except KeyError as e:
                    # Skip the parameter and continue
                    continue
            elif type(parameter) is dict:
                # Iterate through each nested dictionary in the list and extract the values
                try:
                    for key, value in parameter.items():
                        try:
                            if key not in exclude_keys_list:
                                if key == 'schema':
                                    value = parameter['schema']['type']
                                    operation['type'] = value
                                else:
                                    operation[key] = value
                        except KeyError as e:
                            # Skip the parameter and continue
                            continue
                except KeyError as e:
                    # Skip the parameter and continue
                    continue
            doc[f"get_{i}_parameters"] = operation

    # Check for empty keys that will be filtered out later
    if len(doc) == 0:
        return 0
    else:
        return doc


def postParameters(api, path_dictionary):
    """
    Extracts the parameters from the API file for the post request. exclude_keys_list contains
    the keys that are not to be extracted as per the authors are they introduce inconsistencies
    in the data. Extraction needs to be performed for parameters sent as a part of the url as
    well as the http request body.

    :param api: openapi/swagger api specification file.
    :param path_dictionary: contents of the path attribute in the api file.
    :return: dictionary with parameters for the get request.
    """
    doc = dict()
    exclude_keys_list = [
        "description", "title", "default", "example", "readOnly", "writeOnly", "example",
        "title", "enum", "required", "minimum", "maximum", "multipleOf", "minItems", "maxItems"
    ]
    operation_number = 0
    if 'parameters' in path_dictionary['post']:
        # Parse Parameters for post request
        list_of_parameters = path_dictionary['post']['parameters']
        for parameter in list_of_parameters:
            operation = dict()
            if '$ref' in parameter:
                # Its a complexType with value stored as $ref, extract the reference
                ref = parameter['$ref']
                # Access dictionary using value of ref
                ref = ref.split('/')
                ref = ref[-1]

                # Extract the parameters from the reference
                try:
                    parameters = api['components']['parameters'][ref]
                    # Extract the values for the keys in the parameters except the keys in the
                    # exclude_keys_list
                    try:
                        for key, value in parameters.items():
                            if key not in exclude_keys_list:
                                if key == 'schema':
                                    value = api['components']['parameters'][ref]['schema']['type']
                                    operation['type'] = value
                                else:
                                    operation[key] = value
                    except KeyError as e:
                        # Skip the parameter and continue
                        continue
                except KeyError as e:
                    # Skip the parameter and continue
                    continue
            elif type(parameter) is dict:
                # Iterate through each nested dictionary in the list and extract the values
                try:
                    for key, value in parameter.items():
                        try:
                            if key not in exclude_keys_list:
                                if key == 'schema':
                                    value = parameter['schema']['type']
                                    operation['type'] = value
                                else:
                                    operation[key] = value
                        except KeyError as e:
                            # Skip the parameter and continue
                            continue
                except KeyError as e:
                    # Skip the parameter and continue
                    continue
            doc[f"post_{operation_number}_parameters"] = operation
            operation_number += 1

    if 'requestBody' in path_dictionary['post']:
        operation = dict()
        # Parse RequestBody for post request
        if '$ref' in path_dictionary['post']['requestBody']:
            # Go check the schemas for parameters
            ref = path_dictionary['post']['requestBody']['$ref']
            ref = ref.split('/')
            ref = ref[-1]
            try:
                parameters = api['components']['requestBodies'][ref]
                for key, value in parameters.items():
                    if key not in exclude_keys_list:
                        if key == 'schema':
                            value = api['components']['requestBodies'][ref]
                            operation['type'] = value
                        else:
                            operation[key] = value
            except KeyError as e:
                # Skip the parameter and continue
                pass
        else:
            # Iterate through each nested dictionary in the list and extract the values
            try:
                for key, value in path_dictionary['post']['requestBody'].items():
                    try:
                        if key not in exclude_keys_list:
                            if key == 'schema':
                                value = path_dictionary['post']['requestBody']['schema']['type']
                                operation['type'] = value
                            else:
                                operation[key] = value
                    except KeyError as e:
                        # Skip the parameter and continue
                        continue
            except KeyError as e:
                # Skip the parameter and continue
                pass
    # Check for empty keys that will be filtered out later
    if len(doc) == 0:
        return 0
    else:
        return doc


def extractParameters(api_file):
    """
    Extracts the parameters from the API file.

    :param api_file: api file from which the parameters are to be extracted
    :return: document with parameters for each path
    """
    get_doc = dict()
    post_doc = dict()

    path_list = api_file['paths']

    for path in path_list:
        method_type = path_list[path]

        # Check if the get or post request is present in the path
        if 'get' in method_type:
            get_doc[path] = dict()
            dict_of_parameters = getParameters(api_file, method_type)
            # if the list_of_parameters is not empty, add it to the doc
            if dict_of_parameters != 0:
                get_doc[path] = dict_of_parameters
            else:
                get_doc.pop(path)
        if 'post' in method_type:
            # Check if the post request is present in the path
            if 'parameters' or 'requestBody' in method_type['post']:
                dict_of_parameters = postParameters(api_file, method_type)
                post_doc[path] = dict_of_parameters

            # elif 'requestBody' in method_type['post']:
            #     dict_of_parameters = postParameters(api_file, method_type)
            #     post_doc[path] = dict_of_parameters

            # Remove all the keys with a 0 value
            post_doc = {k: v for k, v in post_doc.items() if v}
    return get_doc, post_doc


def unit_test_get_document():
    """
    Unit test for the extractParameters function.
    :return: None
    """
    get_file = 'APIsGuru/openapi.json.2'
    with open(get_file, 'r', encoding='utf-8') as api_file:
        get_data = json.load(api_file)
        get_document, post_document = extractParameters(get_data)
        print(get_document)
        print(post_document)

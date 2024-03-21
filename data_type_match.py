import json
import os
from database import get_collection, post_collection

api_doc_1 = {
    "person_details": {
        "operation_get": {
            "name": "string",
            "age": "int"
        },
        "operation_post": {
            "name": "string",
            "age": "int",
            "in": "query"
        }
    },
    "house_details": {
        "operation_get": {
            "location": "string",
            "price": "int"
        },
        "operation_post": {
            "name": "string",
            "age": "int"
        }
    }
}

api_doc_2 = {
    "girl_details": {
        "operation_get": {
            "name": "string",
            "age": "int",
            "height": "float"
        },
        "operation_post": {
            "name": "string",
            "age": "int",
        }
    },
    "house_details": {
        "operation_get": {
            "name": "string",
            "age": "int",
            "in": "query"
        },
        "operation_post": {
            "name": "string",
            "age": "int"
        }
    }
}

def compare_dicts(dict1, dict2):
    # Get the set of common keys
    common_keys = set(dict1.keys()) & set(dict2.keys())

    # Check if values for common keys are the same in both dictionaries
    for key in common_keys:
        if dict1[key] != dict2[key]:
            return False
    return True


def match_data_types(doc_1, doc_2):
    """
    This function compares the data types of the parameters in the post
    request of doc_1 with the data types of the get request of doc_2
    :param doc_1: first API description
    :param doc_2: second API description
    :return:
    """
    total_match_count = 0

    for method_type in doc_1:
        for operation_type in doc_1[method_type]:
            if "post" in operation_type:
                post_parameters = doc_1[method_type][operation_type]
                for method_type_2 in doc_2:
                    for operation_type_2 in doc_2[method_type_2]:
                        if "get" in operation_type_2:
                            get_parameters = doc_2[method_type_2][operation_type_2]
                            # for all the keys that are common to both post_parameters
                            # and get_parameters, if the values are the same, increment match count by 1
                            if compare_dicts(post_parameters, get_parameters):
                                total_match_count += 1
    return total_match_count


def main():
    print(f"Number of post-get matches = { match_data_types(api_doc_1, api_doc_2)}")


if __name__ == "__main__":
    main()

"""
This script compares the names of the properties of the parameters
"""

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
            "in": "float"
        },
        "operation_post": {
            "name": "string",
            "age": "int",
        }
    },
    "house_details": {
        "operation_get": {
            "name": "string",
            "height": "query"
        },
        "operation_post": {
            "name": "string",
            "age": "int"
        }
    }
}


def compare_dicts(dict1, dict2):
    # if the keys of dict1 are exactly the same as the keys of
    # dict2, return True
    if dict1.keys() == dict2.keys():
        return True


def match_property_names(doc_1, doc_2):
    """
    This function compares the names of the properties of the parameters
    in the post requests of doc_1 against the names of the properties
    of the parameters in doc_2
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
                            # compare the keys of the post parameters with the keys
                            # of the get parameters
                            # if all the keys of the post parameters are in the get
                            # parameters, increment the match count by 1
                            if compare_dicts(post_parameters, get_parameters):
                                total_match_count += 1
    return total_match_count


def main():
    print(f"Number of post-get matches = { match_property_names(api_doc_1, api_doc_2)}")


if __name__ == "__main__":
    main()

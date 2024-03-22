"""
This program compares the data types of the parameters in the post
"""
import json
import os
import time


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
    :return: match count
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


def compare_all_docs():
    """
    This function compares all the documents in the post collection with all the documents in the get collection
    :return: total match count
    """
    num_post_docs_examined = 0
    total_match_count = 0

    # iterate through each document in the post_requests folder found in the local directory
    for filename in os.listdir("post_requests"):
        with open(f"post_requests/{filename}", 'r') as post_file:
            post_doc = json.load(post_file)
            # iterate through each document in the get_requests folder found in the local directory
            for filename in os.listdir("get_requests"):
                with open(f"get_requests/{filename}", 'r') as get_file:
                    get_doc = json.load(get_file)
                    total_match_count += match_data_types(post_doc, get_doc)
            num_post_docs_examined += 1
            print(f"Number of post documents examined: {num_post_docs_examined}")
            print(f"Total match count: {total_match_count}")
            print("--------------------------------------------------")
            print("\n")
    return total_match_count


    # for post_doc in post_collection.find():
    #     print(f"Post doc: {post_doc}")
    #     for get_doc in get_collection.find():
    #         # drop the _id field
    #         post_doc.pop('_id', None)
    #         get_doc.pop('_id', None)
    #         total_match_count += match_data_types(post_doc, get_doc)
    #     num_post_docs_examined += 1
    #     print(f"Number of post documents examined: {num_post_docs_examined}")
    #     print(f"Total match count: {total_match_count}")
    #     print("--------------------------------------------------")
    #     print("\n")
    # return total_match_count


def main():
    start_time = time.time()
    print(f"Number of post-get matches = {compare_all_docs()}")
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    main()

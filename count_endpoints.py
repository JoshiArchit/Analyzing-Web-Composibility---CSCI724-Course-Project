"""
Filename : count_endpoints.py
Author : Archit Joshi (aj6082), Athina Stewart (as1896)
Date Created : 3/22/2024
Description : This script counts the number of nested parameters in the post
and get requests. It also calculates the fraction of data-type matches and
property-name matches.
Link to the original paper: https://ieeexplore.ieee.org/document/9885779
Language : python3
"""

import os
import json


def count_nested_parameters(folder_path):
    """
    This function counts the number of nested parameters in the post and get requests
    :param folder_path: name of the folder containing the post or get requests
    :return: count of the number of nested parameters
    """
    total_nested_params = 0

    # Check if the directory exists
    if os.path.exists(folder_path):
        # Iterate over each file in the directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # Check if the item is a file
            if os.path.isfile(file_path):
                # Load JSON content from the file
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    # Count the number of nested parameters
                    for endpoint_data in data.values():
                        total_nested_params += len(endpoint_data)
    else:
        print("The directory", folder_path, "does not exist.")

    return total_nested_params


def print_stats():
    """
    This function prints the statistics of the number of nested parameters in the post and get requests
    :return: None
    """
    # Define paths to "post" and "get" folders
    post_folder_path = "post_requests"
    get_folder_path = "get_requests"

    # Count nested post parameters
    total_nested_post_params = count_nested_parameters(post_folder_path)
    print("Total number of nested post parameters:", total_nested_post_params)

    # Count nested get parameters
    total_nested_get_params = count_nested_parameters(get_folder_path)
    print("Total number of nested get parameters:", total_nested_get_params)

    percentage_data_type_matches = (43990292/(total_nested_post_params * total_nested_get_params)) * 100
    percentage_property_name_matches = (7587877413/(total_nested_post_params * total_nested_get_params)) * 100


    print(f"Fraction of data-type matches: {round(percentage_data_type_matches, 2)}%")
    print(f"Fraction of property-name matches: {round(percentage_property_name_matches, 2)}%")


def main():
    print_stats()


if __name__ == "__main__":
    main()
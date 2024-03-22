"""
Filename : perform_experiment_from_paper.py
Author : Archit Joshi (aj6082), Athina Stewart (as1896)
Date Created : 3/22/2024
Description : This script performs the experiment mentioned in the original paper.
Link to the original paper: https://ieeexplore.ieee.org/document/9885779
Language : python3
"""

from cleanDataSet import clean_Data_Set
from data_type_match import compare_all_docs as data_type_match
from property_name_match import compare_all_docs as property_name_match
from count_endpoints import print_stats


def perform_matches():
    """
    This function performs the matches between the post and get requests
    Steps:
    1. Clean the dataset. The parameters are extracted from the APIs post and get requests
    and stored in separate files. The files are stored in the post_requests and get_requests folders
    2. Perform the data type matches
    3. Perform the property name matches
    4. Determine the percentage of data type matches and property name matches
    :return: None
    """
    clean_Data_Set()
    print("Data set cleaned.")
    print("Performing data type matches...")
    data_type_match()
    print("Data type matches completed.")
    print("Performing property name matches...")
    property_name_match()
    print("Property name matches completed.")
    print("Calculating percentage data type and property name matches...")
    print_stats()


def main():
    perform_matches()


if __name__ == "__main__":
    main()

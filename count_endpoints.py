import os
import json


def count_nested_parameters(folder_path):
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


def main():
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


if __name__ == "__main__":
    main()
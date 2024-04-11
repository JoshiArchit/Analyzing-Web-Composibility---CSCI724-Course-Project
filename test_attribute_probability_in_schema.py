import os
import json
import sys

def main():
    directory = "APIsGuru"
    files_in_directory = os.listdir(directory)

    swagger_file_count = 0
    swagger_info_description_count = 0
    swagger_basePath_count = 0
    swagger_definitions_count = 0

    openapi_file_count = 0
    openapi_info_description_count = 0

    for file in files_in_directory:
        if "swagger" in file and "json" in file:
            swagger_file_count += 1
            with open("/".join([directory, file])) as file_object:
                json_object = json.load(file_object)
                
                if "info" in json_object and "description" in json_object["info"]:
                    swagger_info_description_count += 1
                if "basePath" in json_object:
                    swagger_basePath_count += 1
                if "definitions" in json_object:
                    swagger_definitions_count += 1
        elif "openapi" in file and "json" in file:
            openapi_file_count += 1
            with open("/".join([directory, file])) as file_object:
                json_object = json.load(file_object)

                if "info" in json_object and "description" in json_object["info"]:
                    openapi_info_description_count += 1
    
    print("Swagger File Count: ", swagger_file_count)
    print("Swagger 'Info-Description' Count: ", swagger_info_description_count)
    print("Swagger 'basePath' Count: ", swagger_basePath_count)
    print("Swagger 'definitions' Count: ", swagger_definitions_count)

    print("OpenAPI File Count: ", openapi_file_count)
    print("OpenAPI 'Info_Description Count': ", openapi_info_description_count)

if __name__ == "__main__":
    main()

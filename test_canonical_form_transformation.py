import os
import json
import os
import sys
from validate_schema_object import validate_schema

CURRENT_SCHEMA_ID = None

def check_info_description(json_object):
    if "info" in json_object:
        if "description" in json_object["info"]:
            if json_object["info"]["description"]:
                return True
    return False

def check_basePath(json_object):
    if "basePath" in json_object:
        if json_object["basePath"]:
            return True
    return False

def check_method_parameters(parameters):
    for parameter in parameters:
        if "name" in parameter:
            if parameter["name"]:
                if "type" in parameter:
                    if parameter["type"]:
                        return True
                elif "schema" in parameter:
                    current_schema = parameter["schema"]
                    if current_schema:
                        if "$ref" in current_schema:
                            if current_schema["$ref"]:
                                return True
                        else:
                            if "properties" in current_schema:
                                properties = current_schema["properties"]
                                for property in properties:
                                    if properties[property]:
                                        property = properties[property]
                                        if property["type"]:
                                            return True
    return False

def get_referenced_schema(json_object, uri):
    if "definitions" in json_object:
        definitions = json_object["definitions"]

        if definitions:
            tokens = uri.split("/")
            tokens = tokens[2:]
            
            current_object = definitions

            for token in tokens:
                current_object = current_object[token]
                
            return current_object
    return None

def resolve_nested_references(current_object, original_object):
    if isinstance(current_object, dict) and "$ref" in current_object:
        return get_referenced_schema(original_object, current_object["$ref"])
    elif isinstance(current_object, dict):
        for key in current_object:
            current_object[key] = resolve_nested_references(current_object[key], original_object)
        return current_object
    else:
        return current_object

def check_produces_consumes(json_object):
    if "paths" in json_object:
        paths = json_object["paths"]

        if len(paths) > 0:
            for path in paths:
                current_path = paths[path]
                if current_path:
                    for method in current_path:
                        current_method = current_path[method]
                
                        if "consumes" in current_method:
                            if "parameters" in current_method and current_method["parameters"]:
                                if check_method_parameters(current_method["parameters"]):
                                    if len(paths) >= 3:
                                            return True
                        if "produces" in current_method:
                                if "responses" in current_method:
                                    responses = current_method["responses"]

                                    if responses:
                                        for response in responses:
                                            if "schema" in response and response["schema"]:
                                                if len(paths) >= 3:
                                                    return True

    return False

def reconstruct_referenced_schemas(json_object):
    paths = json_object["paths"]
    
    for path in paths:
        for method in paths[path]:
            current_method = paths[path][method]
            if "consumes" in current_method:
                if method == "post" or method == "put" or method == "patch":
                    if "parameters" in current_method:
                        parameters = current_method["parameters"]
                        for parameter in parameters:
                            if "in" in parameter and parameter["in"] == "body":
                                current_schema = parameter["schema"]
                                if "$ref" in current_schema:
                                    referenced_schema = get_referenced_schema(json_object, current_schema["$ref"])
                                    if validate_schema(referenced_schema):
                                        write_schema_to_file(method, referenced_schema)
                                else:
                                    if validate_schema(current_schema):
                                        write_schema_to_file(method, current_schema)
                                break
            if "produces" in current_method:
                current_method = paths[path][method]
                for response in current_method["responses"]:
                    if "schema" in response:
                        current_schema = response["schema"]
                        if "$ref" in current_schema:
                            referenced_schema = get_referenced_schema(json_object, current_schema["$ref"])
                            if validate_schema(referenced_schema):
                                write_schema_to_file(method, referenced_schema)
                        else:
                            if validate_schema(current_schema):
                                write_schema_to_file(method, current_schema)

def remove_irrelavant_properties(schema):
    irrelevant_properties_list = ["description", "title", "default", "example", "readOnly", "writeOnly", "example"]
    P_J = ["title", "multipleOf", "maximum", "exclusiveMaximum", "minimum", "exclusiveMinimum", "maxLength", "minLength", "pattern", "maxItems", "minItems", "uniqueItems", "maxProperties", "minProperties", "required", "enum"]
    irrelevant_properties_list.extend(P_J)
    irrelevant_properties_set = set(irrelevant_properties_list)

    for property in irrelevant_properties_set:
        schema.pop(property)

    return schema

def do_canonical_form_transformation(schema):
    schema = remove_irrelavant_properties(schema)
    schema = siplify_complex_operators(schema)
    schema = sort_properties(schema)
    schema = abstract_property_labels(schema)

def write_schema_to_file(method, schema_object):
    global CURRENT_SCHEMA_ID
    file_name = str(CURRENT_SCHEMA_ID) + "_" + method + ".json"
    file_path = os.path.join("reconstructed", file_name)

    with open(file_path, "w") as file:
        json_serialized = json.dumps(schema_object)
        file.write(json_serialized)

    CURRENT_SCHEMA_ID += 1

def main():
    directory = "APIsGuru"
    files_in_directory = os.listdir(directory)

    global CURRENT_SCHEMA_ID 
    CURRENT_SCHEMA_ID = 1

    for file in files_in_directory:
        if "swagger" in file and "json" in file:
            with open("/".join([directory, file])) as file_object:
                json_object = json.load(file_object)
                
                if check_info_description(json_object):
                    if check_basePath(json_object):
                        if check_produces_consumes(json_object):
                                reconstruct_referenced_schemas(json_object)

if __name__ == "__main__":
    main()

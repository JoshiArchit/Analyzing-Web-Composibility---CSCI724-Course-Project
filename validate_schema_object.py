

def validate_schema(json_object):
    """
    This function validates whether an input schema follows the pre-defined rules as set out in the original paper.

    :param json_object: schema to be validated in JSON format
    :return: True if the input schema is valid, False otherwise
    """

    is_valid_schema = True

    P_J = ["title", "multipleOf", "maximum", "exclusiveMaximum", "minimum", "exclusiveMinimum", "maxLength", "minLength", "pattern", "maxItems", "minItems", "uniqueItems", "maxProperties", "minProperties", "required", "enum"]
    P_A = ["type", "allOf", "oneOf", "anyOf", "not", "items", "properties", "additionalProperties", "description", "format", "default"]

    for key in json_object:
        if key in P_J or key in P_A:
            value = json_object[key]

            if isinstance(value, (int, float)):
                if key in P_J and key not in ["title", "pattern", "required", "enum"]:
                    continue
                else:
                    is_valid_schema = False
                    break
            elif isinstance(value, str):
                if key in ["title", "pattern", "type", "format", "description"]:
                    continue
                else:
                    is_valid_schema = False
                    break
            elif isinstance(value, list):
                is_simple_array = True
                for item in value:
                    if not isinstance(item, (int, float, str)):
                        is_simple_array = False
                        break
                if is_simple_array:
                    if key in ["required", "enum"]:
                        continue
                    else:
                        is_valid_schema = False
                        break
                else:
                    if key in P_A and key not in ["type", "format", "description"]:
                        continue
                    else:
                        is_valid_schema = False
                        break
            elif isinstance(value, dict):
                if key in ["properties", "items"]:
                    continue
                else:
                    is_valid_schema = False
                    break
            else:
                is_valid_schema = False
                break
        else:
            is_valid_schema = False
            break
    
    return is_valid_schema

def main():
    test_schema = {"title": 2.0}
    print(validate_schema(test_schema))

if __name__ == "__main__":
    main()

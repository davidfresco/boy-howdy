import json


PRIMITIVE_TYPES = [int, str, float, bool, dict]


def _validate_data_schema(data, schema, path=""):
    # return condition at the end of the schema tree
    if type(schema) is type:
        return True

    # make sure all expected keys are present
    for key in schema.keys():
        if key not in data:
            error = {
                "error": "Request body is missing an attribute",
                "msg:": f"Attribute '{path}.{key}' expected but not found"
            }
            return json.dumps(error), 400

    # check each leaf in the schema
    for key, value in data.items():
        new_path = f"{path}.{key}"

        # unknown key
        if key not in schema:
            error = {
                "error": "Request body does not match schema",
                "msg": f"Attribute '{new_path}' not in schema",
            }
            return json.dumps(error), 400

        # if at leaf, make sure data type is correct
        if schema[key] in PRIMITIVE_TYPES:
            if not isinstance(value, schema[key]):
                error = {
                    "error": "Request body does not match schema",
                    "msg": f"Attribute '{new_path}' with value '{value}' "
                           f"is of type '{type(value).__name__}', not of "
                           f"type '{schema[key].__name__}'",
                }
                return json.dumps(error), 400

        # make sure all leaves are valid too
        subtree_validity = _validate_data_schema(
            value,
            schema[key],
            new_path)
        if subtree_validity is not True:
            return subtree_validity
    return True


class Endpoint:

    def __init__(self, data_schema={}, args_schema=[]):
        self.data_schema = data_schema
        self.args_schema = args_schema

    def validate_data_schema(self, data):
        return _validate_data_schema(data, self.data_schema)

    def execute(self, request):
        data_validity = self.validate_data_schema(request.json)
        if data_validity is not True:
            return data_validity
        return self.run_endpoint(request)

    def run_endpoint(self, request): # pyright: ignore
        return "", 200


# unit tests for request schema validation
if __name__ == "__main__":
    schema = {
        "body": {
            "data": dict,
            "integer": int
        },
        "footer": str
    }
    good_data = {"body":{"data":{"value1":1,"val2":2,},"integer":2,},
                 "footer":"message lol"}
    bad_dict = {"body":{"data":"dict","integer":2,},"footer":"message lol"}
    bad_int = {"body":{"data":{"value1":1,"val2":2,},"integer":"a",},
               "footer":"message lol"}
    bad_str = {"body":{"data":{"value1":1,"val2":2,},"integer":1,},"footer":5}
    unknown_key = {"header":{},"body":{"data":{"value1":1,"val2":2,},
                                       "integer":1,},"footer":5}
    missing_key = {"body":{"data":{"value1":1,"val2":2,}},"footer":"sdfg"}

    endpoint = Endpoint(data_schema=schema)
    print(endpoint.validate_data_schema(good_data))
    print(endpoint.validate_data_schema(bad_dict))
    print(endpoint.validate_data_schema(bad_int))
    print(endpoint.validate_data_schema(bad_str))
    print(endpoint.validate_data_schema(unknown_key))
    print(endpoint.validate_data_schema(missing_key))

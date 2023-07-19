from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name"],
}

validate(instance={"name": "John", "age": 30}, schema=schema)
# No error, the JSON is valid.

#validate(instance={"name": "John", "age": "30"}, schema=schema)
# ValidationError: '30' is not of type 'number'

validate(instance={"name": "John"}, schema=schema)
# No error, the JSON is valid.

#validate(instance={"age": 30}, schema=schema)
# ValidationError: 'name' is a required property

validate(instance={"name": "John", "age": 30, "job": "Engineer"}, schema=schema)
# No error, the JSON is valid. By additional fields are allowed.
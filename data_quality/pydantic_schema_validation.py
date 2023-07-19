import pydantic
from pydantic import BaseModel

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name"],
}

class ExampleSchema(BaseModel):
    """Schema for Example dict"""
    type: str 
    properties: dict
    name: dict 
    age: dict 
    required: list[str]

def validate(obj: dict):
    validation_error_count = 0
    try:
        ExampleSchema.model_validate(obj)
        validation_error_count += 1
    except ValueError as e:
        print(f"Error found in object: ", e.json())
    print(f"Validation Error Count: {validation_error_count}")
    

validate(schema)
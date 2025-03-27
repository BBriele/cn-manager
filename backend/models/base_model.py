import uuid
from datetime import datetime

class BaseModel:
    schema = {
        'id': {'type': str, 'required': True},
        'created_at': {'type': datetime, 'required': True},
        'updated_at': {'type': datetime, 'required': True},
        # Add other fields and their constraints here
    }

    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        print("base_mode pre validate")
        self.validate()  # Validate the instance variables
        print("base_mode middle init")
        for key, value in kwargs.items():
            if key in self.schema:  # Only set attributes defined in the schema
                setattr(self, key, value)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at),
        }

    def validate(self):
        """
        Validates the instance variables against the schema.
        """
        print("base_mode start validate")
        for field, constraints in self.schema.items():
            if not hasattr(self, field) and constraints.get('required', False):
                raise ValueError(f"Field '{field}' is required")
            if hasattr(self, field):
                print("base_mode hasattr validate")
                value = getattr(self, field)
                print(value)
                if 'type' in constraints and not isinstance(value, constraints['type']):
                    raise TypeError(f"Field '{field}' must be of type {constraints['type']}")
                if 'validator' in constraints:
                    constraints['validator'](value)

    @classmethod
    def get_by(cls, items, attribute, value):
        """
        Generic method to get items by a specific attribute.
        """
        return [item for item in items if getattr(item, attribute) == value]
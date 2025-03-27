import uuid
import datetime
from models.base_model import BaseModel

class Domain(BaseModel):
    model_name = "domains"  # Define the model name
    schema = {
        **BaseModel.schema,
        'name': {'type': str, 'required': True}
    }

    def __init__(self, **kwargs):
        print(kwargs.items())
        self.name = kwargs.get('name')
        super().__init__(**kwargs)

    def __str__(self):
        return self.name

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        data = super().to_dict()
        data['name'] = self.name
        return data

    @classmethod
    def get_by_name(cls, items, name):
        """
        Specific method to get domains by name.
        """
        return cls.get_by(items, 'name', name)

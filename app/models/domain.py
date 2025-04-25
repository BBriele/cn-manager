from datetime import datetime

from utility import db
from models.base_model import BaseModel

class Domain(BaseModel):
    model_name = "domains"  # Define the model name

    schema = {
        **BaseModel.schema,  # Include inherited fields
        'name': {'type': str, 'required': True}
    }

    def __init__(self, **kwargs):
        """
        Initialize the Domain model, calling the parent constructor.
        """
        super().__init__(**kwargs)  # BaseModel already assigns `name` from kwargs

    def __str__(self):
        return self.name

    def get_name(self) -> str:
        """
        Get the domain name.
        """
        return self.name

    def set_name(self, name: str):
        """
        Update the domain name and set the updated_at timestamp.
        """
        self.name = name
        self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self):
        """
        Convert the Domain object into a dictionary.
        """
        data = super().to_dict()
        data['name'] = self.name
        return data

    @classmethod
    def get_by_name(cls, name):
        """
        Retrieve a domain from the database by its name.
        """
        return db.read(cls.model_name, {'name': name})

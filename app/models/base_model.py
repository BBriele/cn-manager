import uuid
from datetime import datetime
from db_manager import db  # Usa il database manager globale

class BaseModel:
    schema = {
        'id': {'type': str, 'required': True},
        'created_at': {'type': datetime, 'required': True},
        'updated_at': {'type': datetime, 'required': True},
    }

    model_name = None  # Ogni modello figlio deve definirlo

    def __init__(self, **kwargs):
        """
        Initialize the model with default values and any provided keyword arguments.
        """
        self.id = str(uuid.uuid4())
        #set the default values for the created_at and updated_at in timestamp format
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if key in self.schema:  # Ensure only allowed attributes are set
                setattr(self, key, value)


        self.validate()  # Validate the instance

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
    
    def items(self):
        """
        Return the items of the object.
        """
        return self.__dict__.items()

    def to_dict(self):
        """
        Convert the object into a dictionary.
        """
        
        return self.__dict__.items()


    def validate(self):
        """
        Validate the instance variables based on the schema.
        """
        for field, constraints in self.schema.items():
            if not hasattr(self, field) and constraints.get('required', False):
                raise ValueError(f"Field '{field}' is required")
            if hasattr(self, field):
                value = getattr(self, field)
                if 'type' in constraints and not isinstance(value, constraints['type']): 
                    raise TypeError(f"Field '{field}' must be of type {constraints['type']}")
                if 'validator' in constraints:
                    constraints['validator'](value)

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new instance and save it to the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        instance = cls(**kwargs)
        db.create(cls.model_name, instance.to_dict())
        return instance

    @classmethod
    def get(cls, item_id: str):
        """
        Retrieve an item from the database by its ID.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")

        results = db.read(cls.model_name, {'id': item_id})
        return results[0] if results else None

    @classmethod
    def update(cls, item_id: str, **kwargs):
        """
        Update an item in the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        kwargs['updated_at'] = datetime.utcnow().isoformat()  # Update timestamp
        return db.update(cls.model_name, {'id': item_id}, kwargs)

    @classmethod
    def delete(cls, item_id: str):
        """
        Delete an item from the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        return db.delete(cls.model_name, {'id': item_id})

    @classmethod
    def list(cls):
        """
        List all items of this model from the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        return db.read(cls.model_name)
    
    
    def to_json(self):
        """
        Convert the object in JSON-serializable.
        """
        x = {}
        for key in self.schema.keys():
            if getattr(self, key):
                x[key] = getattr(self, key)
        #convert the datetime to string
        for key, value in x.items():
            if isinstance(value, datetime):
                x[key] = value.isoformat()
                
        return x
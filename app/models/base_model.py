import uuid
from datetime import datetime
from utility import db, logger  # Usa il database manager globale

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
        logger.info(f"Initializing BaseModel for {self.model_name}")
        self.id = str(uuid.uuid4())
        #set the default values for the created_at and updated_at in timestamp format
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if key in self.schema:  # Ensure only allowed attributes are set
                setattr(self, key, value)

        logger.info(f"BaseModel initialized with id: {self.id}")

        try:
            self.validate()  # Validate the instance
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return False
        except TypeError as e:
            logger.error(f"Type error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False

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
        logger.info(f"Validation Model schemea: {self.schema}") 
        for field, constraints in self.schema.items():
            if not hasattr(self, field) and constraints.get('required', False):
                raise ValueError(f"Field '{field}' is required")
            if hasattr(self, field):
                value = getattr(self, field)
                if 'type' in constraints:
                    # Handle multiple types
                    if isinstance(constraints['type'], tuple):
                        if not isinstance(value, constraints['type']):
                            raise TypeError(f"Field '{field}' must be one of the following types: {constraints['type']}")
                    elif not isinstance(value, constraints['type']): 
                        raise TypeError(f"Field '{field}' must be of type {constraints['type']}")
                if 'validator' in constraints:
                    constraints['validator'](value)
        logger.info(f"BaseModel validated with id: {self.id}")

    @classmethod
    def create(cls, **kwargs):
        """
        Create a new instance and save it to the database.
        """
        logger.info(f"Starting the creation of {cls.__name__} with data: {kwargs}")
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        try:
            instance = cls(**kwargs)
        except (ValueError, TypeError) as e:
            logger.error(f"Validation error during creation of {cls.__name__}: {e}")
            return None  # Or return a default/error object

        #print("instanza create", instance.to_dict())
        db.create(cls.model_name, instance)
        logger.info(f"{cls.__name__} created with id: {instance.id}")
        return instance

    @classmethod
    def get(cls, item_id: str):
        """
        Retrieve an item from the database by its ID.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")

        results = db.read(cls.model_name, {'id': item_id})
        if results:
            logger.info(f"{cls.__name__} retrieved with id: {item_id}")
            return results[0] 
        else:
            logger.warning(f"{cls.__name__} not found with id: {item_id}")
            return None

    @classmethod
    def update(cls, item_id: str, **kwargs):
        """
        Update an item in the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        kwargs['updated_at'] = datetime.utcnow().isoformat()  # Update timestamp
        result = db.update(cls.model_name, {'id': item_id}, kwargs)
        logger.info(f"{cls.__name__} updated with id: {item_id}")
        return result

    @classmethod
    def delete(cls, item_id: str):
        """
        Delete an item from the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        result = db.delete(cls.model_name, {'id': item_id})
        logger.info(f"{cls.__name__} deleted with id: {item_id}")
        return result

    @classmethod
    def list(cls):
        """
        List all items of this model from the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        results =  db.read(cls.model_name)
        logger.info(f"{cls.__name__} list called, returning {len(results)} items")
        return results
    
    @classmethod
    def get_all(cls):
        """
        Get all items of this model from the database.
        """
        if cls.model_name is None:
            raise ValueError("model_name must be defined in the child class")
        
        results = db.read(cls.model_name)
        logger.info(f"{cls.__name__} get_all called, returning {len(results)} items")
        return results
    
    
    def to_json(self):
        """
        Convert the object in JSON-serializable.
        """
        logger.info(f"Converting {self.__class__.__name__} with id {self.id} to JSON")
        x = {}
        for key in self.schema.keys():
            if hasattr(self, key) and getattr(self, key) is not None:
                x[key] = getattr(self, key)
                logger.debug(f"Adding key {key} with value {x[key]} to JSON")
            else:
                logger.debug(f"Skipping key {key} as it is None or not present")
        #convert the datetime to string
        for key, value in x.items():
            if isinstance(value, datetime):
                x[key] = value.isoformat()
                logger.debug(f"Converting datetime {key} to ISO format: {x[key]}")
                
        logger.info(f"Conversion of {self.__class__.__name__} with id {self.id} to JSON complete")
        return x
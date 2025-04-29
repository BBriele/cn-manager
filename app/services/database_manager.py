import json
import os
from typing import Any, Dict, List, Optional

class DatabaseManager:
    """
    A simple JSON-based database manager that supports CRUD operations generically,
    handling multiple entity types dynamically based on their schema.
    """

    def __init__(self, filename = os.environ.get('DATABASE_FILE', 'database.json')) -> None:
        """
        Initialize the DatabaseManager with the given filename.
        """
        self.filename = filename
        self._ensure_file()

    def _ensure_file(self) -> None:
        """
        Ensure the JSON file exists; if not, create an empty JSON structure.
        """
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4)

    def _read_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Read the JSON file and return the data as a dictionary.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def _write_data(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        """
        Write the given data dictionary back to the JSON file.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def create(self, entity_type: str, record: Dict[str, Any]) -> None:
        """
        Add a new record to the specified entity type.
        """
        data = self._read_data()
        

        #if in data there is no entity_type, create it
        if entity_type not in data:
            data[entity_type] = []
            
        data[entity_type].append(record.to_json())
        self._write_data(data)

    def read(self, entity_type: str, filter_by: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve records of a specific entity type, optionally filtering them.
        """
        data = self._read_data()
        records = data.get(entity_type, [])

        if filter_by:
            records = [r for r in records if all(r.get(k) == v for k, v in filter_by.items())]
        
        return records

    def update(self, entity_type: str, identifier: Dict[str, Any], updated_data: Dict[str, Any]) -> bool:
        """
        Update an existing record by matching it with an identifier.
        Returns True if the update was successful, otherwise False.
        """
        data = self._read_data()
        records = data.get(entity_type, [])
        
        for record in records:
            if all(record.get(k) == v for k, v in identifier.items()):
                record.update(updated_data)
                self._write_data(data)
                return True
        
        return False

    def delete(self, entity_type: str, identifier: Dict[str, Any]) -> bool:
        """
        Delete a record by matching it with an identifier.
        Returns True if deletion was successful, otherwise False.
        """
        data = self._read_data()
        records = data.get(entity_type, [])
        
        new_records = [r for r in records if not all(r.get(k) == v for k, v in identifier.items())]
        
        if len(new_records) != len(records):
            data[entity_type] = new_records
            self._write_data(data)
            return True
        
        return False
    
    
    def list(self, entity_type: str) -> List[Dict[str, Any]]:
        """
        List all records of a specific entity type.
        """
        return self.read(entity_type)
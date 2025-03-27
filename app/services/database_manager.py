import json
from typing import List, Dict, Type, Optional
from models.base_model import BaseModel
from models.domain import Domain
from models.dns_config import DNSConfig
from models.certificate import Certificate
from models.nginx_config import NginxConfig
from models.proxy_rule import ProxyRule
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

MODEL_MAP = {
    "domains": Domain,
    "dns_configs": DNSConfig,
    "certificates": Certificate,
    "nginx_configs": NginxConfig,
    "proxy_rules": ProxyRule,
}

class DatabaseManager:
    def __init__(self, db_file: str = 'db.json'):
        self.db_file = db_file
        # Logging: Database initialization
        logger.info(f"Initializing DatabaseManager with db_file: {self.db_file}")
        self.data: Dict[str, Dict[str, dict]] = self._load_data()

    def _load_data(self) -> Dict[str, Dict[str, dict]]:
        # Logging: Loading data from database
        logger.info(f"Loading data from database file: {self.db_file}")
        try:
            with open(self.db_file, 'r') as f:
                try:
                    data = json.load(f)
                    # Convert data to the correct format
                    for model_name, items in data.items():
                        if not isinstance(items, dict):
                            data[model_name] = {}
                    # Logging: Data loaded successfully
                    logger.info(f"Data loaded successfully from {self.db_file}")
                    return data
                except json.JSONDecodeError:
                    # Logging: Invalid JSON in database file
                    logger.warning(f"Invalid JSON in database file: {self.db_file}. Returning empty dictionary.")
                    return {}
        except FileNotFoundError:
            # Logging: Database file not found
            logger.warning(f"Database file not found: {self.db_file}")
            return {}

    def _save_data(self):
        # Logging: Saving data to database
        logger.info(f"Saving data to database file: {self.db_file}")
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)
        # Logging: Data saved successfully
        logger.info(f"Data saved successfully to {self.db_file}")

    def create(self, model_name: str, item: BaseModel):
        # Logging: Creating a new item
        print("quii2")
        logger.info(f"Creating a new item in {model_name}: {item.id}")
        if model_name not in self.data:
            self.data[model_name] = {}

        item_id = item.id
        self.data[model_name][item_id] = item.to_dict()
        self._save_data()
        # Logging: Item created successfully
        logger.info(f"Item created successfully in {model_name}: {item.id}")

    def get(self, model_name: str, item_id: str) -> Optional[BaseModel]:
        # Logging: Getting an item
        logger.info(f"Getting item {item_id} from {model_name}")
        if model_name in self.data and item_id in self.data[model_name]:
            model_data = self.data[model_name][item_id]
            model_class = MODEL_MAP.get(model_name)
            if model_class:
                # Logging: Item found
                logger.info(f"Item {item_id} found in {model_name}")
                return model_class(**model_data)
        # Logging: Item not found
        logger.warning(f"Item {item_id} not found in {model_name}")
        return None

    def update(self, model_name: str, item_id: str, item: BaseModel):
        # Logging: Updating an item
        logger.info(f"Updating item {item_id} in {model_name}")
        if model_name in self.data and item_id in self.data[model_name]:
            item.updated_at = datetime.utcnow()
            self.data[model_name][item_id] = item.to_dict()
            self._save_data()
            # Logging: Item updated successfully
            logger.info(f"Item {item_id} updated successfully in {model_name}")
        else:
            # Logging: Item not found for update
            logger.error(f"Item with id {item_id} not found in {model_name} for update")
            raise ValueError(f"Item with id {item_id} not found in {model_name}")

    def delete(self, model_name: str, item_id: str):
        # Logging: Deleting an item
        logger.info(f"Deleting item {item_id} from {model_name}")
        if model_name in self.data and item_id in self.data[model_name]:
            del self.data[model_name][item_id]
            self._save_data()
            # Logging: Item deleted successfully
            logger.info(f"Item {item_id} deleted successfully from {model_name}")
        else:
            # Logging: Item not found for deletion
            logger.error(f"Item with id {item_id} not found in {model_name} for deletion")
            raise ValueError(f"Item with id {item_id} not found in {model_name}")

    def list(self, model_name: str) -> List[BaseModel]:
        # Logging: Listing items
        logger.info(f"Listing items from {model_name}")
        if model_name in self.data:
            model_class = MODEL_MAP.get(model_name)
            if model_class:
                # Logging: Items listed successfully
                logger.info(f"Items listed successfully from {model_name}")
                return [model_class(**item) for item in self.data[model_name].values()]
        # Logging: No items found
        logger.warning(f"No items found in {model_name}")
        return []
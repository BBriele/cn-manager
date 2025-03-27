import json
from typing import List, Dict, Type, Optional
from pydantic import BaseModel
from models.domain import Domain
from models.cloudflare import CloudflareConfig
from models.certificate import Certificate
from models.nginx_config import NginxConfig
from models.proxy_rule import ProxyRule

MODEL_MAP = {
    "domains": Domain,
    "cloudflare_configs": CloudflareConfig,
    "certificates": Certificate,
    "nginx_configs": NginxConfig,
    "proxy_rules": ProxyRule,
}

class DatabaseManager:
    def __init__(self, db_file: str = 'cn_manager_db.json'):
        self.db_file = db_file
        self.data: Dict[str, Dict[str, dict]] = self._load_data()

    def _load_data(self) -> Dict[str, Dict[str, dict]]:
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
                # Convert data to the correct format
                for model_name, items in data.items():
                    if not isinstance(items, dict):
                        data[model_name] = {}
                return data
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def create(self, model_name: str, item: BaseModel):
        if model_name not in self.data:
            self.data[model_name] = {}

        item_id = item.id
        self.data[model_name][item_id] = item.model_dump()
        self._save_data()

    def get(self, model_name: str, item_id: str) -> Optional[BaseModel]:
        if model_name in self.data and item_id in self.data[model_name]:
            model_data = self.data[model_name][item_id]
            model_class = MODEL_MAP.get(model_name)
            if model_class:
                return model_class(**model_data)
        return None

    def update(self, model_name: str, item_id: str, item: BaseModel):
        if model_name in self.data and item_id in self.data[model_name]:
            self.data[model_name][item_id] = item.model_dump()
            self._save_data()
        else:
            raise ValueError(f"Item with id {item_id} not found in {model_name}")

    def delete(self, model_name: str, item_id: str):
        if model_name in self.data and item_id in self.data[model_name]:
            del self.data[model_name][item_id]
            self._save_data()
        else:
            raise ValueError(f"Item with id {item_id} not found in {model_name}")

    def list(self, model_name: str) -> List[BaseModel]:
        if model_name in self.data:
            model_class = MODEL_MAP.get(model_name)
            if model_class:
                return [model_class(**item) for item in self.data[model_name].values()]
        return []
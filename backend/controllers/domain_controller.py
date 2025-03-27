from models.domain import Domain
from services.database_manager import DatabaseManager

db_manager = DatabaseManager()

def create_domain(domain_data: dict) -> Domain:
    """
    Creates a new domain and saves it to the database.
    """
    try:
        domain = Domain(**domain_data)
        db_manager.create("domains", domain)
        return domain
    except Exception as e:
        raise e

def get_domain(domain_id: str) -> Domain:
    """
    Retrieves a domain from the database.
    """
    domain = db_manager.get("domains", domain_id)
    if not domain:
        raise ValueError(f"Domain with id {domain_id} not found")
    return domain

def update_domain(domain_id: str, domain_data: dict) -> Domain:
    """
    Updates an existing domain in the database.
    """
    try:
        domain = Domain(**domain_data)
        db_manager.update("domains", domain_id, domain)
        return domain
    except Exception as e:
        raise e

def delete_domain(domain_id: str):
    """
    Deletes a domain from the database.
    """
    db_manager.delete("domains", domain_id)

def list_domains() -> list[Domain]:
    """
    Lists all domains from the database.
    """
    return db_manager.list("domains")
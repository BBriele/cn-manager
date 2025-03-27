from models.domain import Domain
from services.database_manager import DatabaseManager
import logging

logger = logging.getLogger(__name__)

db_manager = DatabaseManager()

class DomainController:
    """
    DomainController is responsible for managing domain-related operations.
    It provides methods to create, retrieve, update, delete, and list domains.
    """
    def __init__(self):
        """
        Initializes the DomainController.
        """
    def create_domain(domain_data: dict) -> Domain:
        # Logging: Creating domain
        logger.info(f"Creating domain with data: {domain_data}")
        """
        Creates a new domain and saves it to the database.
        """
        try:
            print(domain_data)
            domain = Domain(**domain_data)
            db_manager.create("domains", domain)
            # Logging: Domain created successfully
            logger.info(f"Domain created successfully: {domain.id}")
            return domain
        except Exception as e:
            # Logging: Error creating domain
            logger.error(f"Error creating domain: {e}")
            raise e

    def get_domain(domain_id: str) -> Domain:
        # Logging: Getting domain
        logger.info(f"Getting domain with id: {domain_id}")
        """
        Retrieves a domain from the database.
        """
        domain = db_manager.get("domains", domain_id)
        if not domain:
            # Logging: Domain not found
            logger.warning(f"Domain with id {domain_id} not found")
            raise ValueError(f"Domain with id {domain_id} not found")
        # Logging: Domain found
        logger.info(f"Domain found: {domain.id}")
        return domain

    def update_domain(domain_id: str, domain_data: dict) -> Domain:
        # Logging: Updating domain
        logger.info(f"Updating domain with id {domain_id} and data: {domain_data}")
        """
        Updates an existing domain in the database.
        """
        try:
            domain = Domain(**domain_data)
            db_manager.update("domains", domain_id, domain)
            # Logging: Domain updated successfully
            logger.info(f"Domain updated successfully: {domain.id}")
            return domain
        except Exception as e:
            # Logging: Error updating domain
            logger.error(f"Error updating domain: {e}")
            raise e

    def delete_domain(domain_id: str):
        # Logging: Deleting domain
        logger.info(f"Deleting domain with id: {domain_id}")
        """
        Deletes a domain from the database.
        """
        db_manager.delete("domains", domain_id)
        # Logging: Domain deleted successfully
        logger.info(f"Domain deleted successfully: {domain_id}")

    def list_domains() -> list[Domain]:
        # Logging: Listing domains
        logger.info("Listing domains")
        """
        Lists all domains from the database.
        """
        domains = db_manager.list("domains")
        # Logging: Domains listed successfully
        logger.info(f"Listed {len(domains)} domains")
        return domains

    def get_domain_by_name(domain_name: str) -> Domain:
        # Logging: Getting domain by name
        logger.info(f"Getting domain with name: {domain_name}")
        """
        Retrieves a domain from the database by name.
        """
        domains = list_domains()
        domain = Domain.get_by_name(domains, domain_name)
        if not domain:
            # Logging: Domain not found
            logger.warning(f"Domain with name {domain_name} not found")
            raise ValueError(f"Domain with name {domain_name} not found")
        # Logging: Domain found
        logger.info(f"Domain found: {domain.id}")
        return domain[0]
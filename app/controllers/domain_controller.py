from flask import Blueprint, render_template, request, redirect, url_for
import logging

from models.domain import Domain
from db_manager import db  # Usa il database manager globale


# Configure logging
log_file = 'cn_manager.log'
log_level = logging.INFO
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)

# Create a formatter
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


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
            db.create("domains", domain)
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
        domain = db.get("domains", domain_id)
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
            db.update("domains", domain_id, domain)
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
        db.delete("domains", domain_id)
        # Logging: Domain deleted successfully
        logger.info(f"Domain deleted successfully: {domain_id}")

    def list_domains() -> list[Domain]:
        # Logging: Listing domains
        logger.info("Listing domains")
        """
        Lists all domains from the database.
        """
        domains = db.list("domains")
        # Logging: Domains listed successfully
        logger.info(f"Listed {len(domains)} domains")
        return domains

    def get_domain_by_name(domain_name: str) -> Domain:
        # Logging: Getting domain by name
        logger.info(f"Getting domain with name: {domain_name}")
        """
        Retrieves a domain from the database by name.
        """
        domains = db()
        domain = Domain.get_by_name(domains, domain_name)
        if not domain:
            # Logging: Domain not found
            logger.warning(f"Domain with name {domain_name} not found")
            raise ValueError(f"Domain with name {domain_name} not found")
        # Logging: Domain found
        logger.info(f"Domain found: {domain.id}")
        return domain[0]

#region View Functions

    def view_domain_list():
        #logging: Rendering domain list view
        logger.info("Rendering domain list view")
        """
        Renders the domain list view.
        """
        domains = db.list("domains")
        return render_template('domain/list.html', domains=domains)


#endregion


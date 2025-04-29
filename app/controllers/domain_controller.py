from flask import Blueprint, render_template, request, redirect, url_for
import logging

from models.domain import Domain
from utility import db, logger  # Usa il database manager globale



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
            domain = Domain(**domain_data)
            db.create("domains", domain)

            logger.info(f"Domain created successfully: {domain.id}")
            return domain
        except Exception as e:
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

    def list_view():
        #logging: Rendering domain list view
        logger.info("Rendering domain list view")
        """
        Renders the domain list view.
        """
        domains = db.list("domains")
        return render_template('components/domain/list.html', domains=domains)
    
    @classmethod
    def create_view(cls, request):
        #logging: Rendering create domain view
        logger.info("Rendering create domain view")
        """
        Renders the create domain view.
        """
        if request.method == 'POST':
            try:
                domain_data = {
                    "name": request.form['name']
                }
                cls.create_domain(domain_data)
                return redirect(url_for('domain.list'))
            except Exception as e:
                return render_template('components/domain/create.html', errors=[str(e)])

        return render_template('components/domain/create.html', errors=None)


#endregion


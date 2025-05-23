from flask import Blueprint, render_template, request, redirect, url_for

from models.certificate import Certificate
from services.cert_manager import CertManager  # Assuming you'll have a CertManager
from utility import db, logger  # Usa il database manager globale

cert_manager = CertManager()  # Initialize CertManager

class CertificateController:
    """
    Controller for managing certificates.
    This controller handles the creation, retrieval, updating, and deletion of certificates.
    It interacts with the database manager and the certificate manager to perform these operations.
    """    
    def create_certificate(certificate_data: dict):
        """
        Creates a new certificate and saves it to the database.
        """
        try:
            certificate = Certificate(**certificate_data)
            
            db.create("certificates", certificate)

            # Generate the certificate using CertManager
            #cert_manager.generate_certificate(certificate)

            return True
        except Exception as e:
            raise e

    def get_certificate(certificate_id: str):
        """
        Retrieves a certificate from the database.
        """
        return db.get("certificates", certificate_id)

    def update_certificate(certificate_id: str, certificate_data: dict):
        """
        Updates an existing certificate in the database.
        """
        try:
            certificate = Certificate(**certificate_data)
            db.update("certificates", certificate_id, certificate)
            return certificate
        except Exception as e:
            raise e

    def delete_certificate(certificate_id: str):
        """
        Deletes a certificate from the database.
        """
        db.delete("certificates", certificate_id)


#region View Functions

    def list_view():
        """
        Renders the list view of certificates.
        """
        logger.info("Rendering certificate list view")
        certificates = db.list("certificates")
        domains = db.list("domains")

        return render_template('components/certificate/list.html', certificates=certificates, domains=domains)
    
    @classmethod
    def create_view(cls, request):
        """
        Renders the create certificate view.
        """
        if request.method == 'POST':

            try:
                logger.info("Creating certificate")

                certificate_data = request.form.to_dict() 
                certificate_data["dns_challenge"] = bool(certificate_data["dns_challenge"])           

                cls.create_certificate(certificate_data)
                return redirect(url_for('certificate.list'))
            except Exception as e:
                return render_template('components/certificate/create.html', errors=[str(e)])
            
        logger.info("Rendering create certificate view")
        domains = db.list("domains")
        return render_template('components/certificate/create.html', domains = domains, errors=None)
    
    def edit_view(certificate_id: str):
        """
        Renders the edit view for a specific certificate.
        """
        certificate = db.get("certificates", certificate_id)
        domains = db.list("domains")
        return render_template('components/certificate/edit.html', certificate=certificate, domains=domains)
    
    def delete_view(request: str):   
        """
        Deletes a certificate and redirects to the list view.
        """
        #get the certificate id from the request
        certificate_id = request.args.get("id")

        identifier = {"id": certificate_id}
        db.delete("certificates", identifier)
        return redirect(url_for('certificate.list'))
    
#endregion
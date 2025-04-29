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
            cert_manager.generate_certificate(certificate)

            # Update the certificate in the database with the generated paths
            updated_certificate = db.get("certificates", certificate.id)
            db.update("certificates", certificate.id, updated_certificate)

            return updated_certificate
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
        certificates = db.list("certificates")
        print(certificates)
        return render_template('components/certificate/list.html', certificates=certificates)
    
    @classmethod
    def create_view(cls, request):
        #logging: Rendering create certificate view
        logger.info("Rendering create certificate view")
        """
        Renders the create certificate view.
        """
        if request.method == 'POST':
            try:
                certificate_data = request.form.to_dict()
                

                cls.create_certificate(certificate_data)
                return redirect(url_for('certificate.list'))
            except Exception as e:
                return render_template('components/certificate/create.html', errors=[str(e)])
        domains = db.list("domains")
        return render_template('components/certificate/create.html', domains = domains, errors=None)
    
    def edit_view(certificate_id: str):
        """
        Renders the edit view for a specific certificate.
        """
        certificate = db.get("certificates", certificate_id)
        domains = db.list("domains")
        return render_template('components/certificate/edit.html', certificate=certificate, domains=domains)

#endregion
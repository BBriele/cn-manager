from models.certificate import Certificate
from services.database_manager import DatabaseManager
from services.cert_manager import CertManager  # Assuming you'll have a CertManager

db_manager = DatabaseManager()
cert_manager = CertManager()  # Initialize CertManager

def create_certificate(certificate_data: dict):
    """
    Creates a new certificate and saves it to the database.
    """
    try:
        certificate = Certificate(**certificate_data)
        db_manager.create("certificates", certificate)

        # Generate the certificate using CertManager
        cert_manager.generate_certificate(certificate)

        # Update the certificate in the database with the generated paths
        updated_certificate = db_manager.get("certificates", certificate.id)
        db_manager.update("certificates", certificate.id, updated_certificate)

        return updated_certificate
    except Exception as e:
        raise e

def get_certificate(certificate_id: str):
    """
    Retrieves a certificate from the database.
    """
    return db_manager.get("certificates", certificate_id)

def update_certificate(certificate_id: str, certificate_data: dict):
    """
    Updates an existing certificate in the database.
    """
    try:
        certificate = Certificate(**certificate_data)
        db_manager.update("certificates", certificate_id, certificate)
        return certificate
    except Exception as e:
        raise e

def delete_certificate(certificate_id: str):
    """
    Deletes a certificate from the database.
    """
    db_manager.delete("certificates", certificate_id)
# CN Manager

## Project Overview

CN Manager is a Python-based application designed to simplify the management of certificates, domains, and Nginx configurations. It provides a user-friendly interface for creating, updating, and deleting these resources, automating tasks such as SSL certificate generation and Nginx configuration file management.

## Features

### Implemented

*   **Domain Management:**
    *   Create, list, update, and delete domains.
    *   Uses a [database manager](app/services/database_manager.py) for persistence.
    *   [Domain model](app/models/domain.py) defines the structure of a domain.
    *   [Domain controller](app/controllers/domain_controller.py) handles business logic.
    *   [Routes](app/routes/domain.py) expose domain management endpoints.
    *   Templates for listing ([domain_list.html](app/templates/domain_list.html)) and creating ([domain_create.html](app/templates/domain_create.html)) domains.
*   **Nginx Configuration Management:**
    *   Create, list, update, and delete Nginx configurations.
    *   Uses a [database manager](app/services/database_manager.py) for persistence.
    *   [NginxConfig model](app/models/nginx_config.py) defines the structure of an Nginx configuration.
    *   [NginxManager service](app/services/nginx_manager.py) handles Nginx configuration file generation and reloading.
    *   [Routes](app/routes/config.py) expose Nginx configuration management endpoints.
    *   Template for listing configurations ([config_list.html](app/templates/config_list.html)).
*   **SSL Certificate Management:**
    *   Generate SSL certificates using Certbot.
    *   Uses a [database manager](app/services/database_manager.py) for persistence.
    *   [Certificate model](app/models/certificate.py) defines the structure of a certificate.
    *   [CertManager service](app/services/cert_manager.py) handles certificate generation using Certbot.
    *   [Routes](app/routes/certs.py) expose certificate management endpoints.
*   **DNS Configuration Management:**
    *   Create, list, update, and delete DNS configurations.
    *   Supports multiple DNS providers (Cloudflare, AWS Route53, Google Cloud DNS).
    *   Uses a [database manager](app/services/database_manager.py) for persistence.
    *   [DNSConfig model](app/models/dns_config.py) defines the structure of a DNS configuration.
    *   [DNSConfigController](app/controllers/dns_config_controller.py) handles business logic.
    *   [Routes](app/routes/dns_config.py) expose DNS configuration management endpoints.
    *   Templates for listing ([dns_config/list.html](app/templates/dns_config/list.html)), creating ([dns_config/create.html](app/templates/dns_config/create.html)), and updating ([dns_config/update.html](app/templates/dns_config/update.html)) DNS configurations.
*   **Custom DNS Provider Plugins:**
    *   Dynamically load custom DNS provider plugins from the `plugins/custom_dns` directory.
    *   [DNSProvider model](app/models/dns_provider.py) defines the interface for DNS providers.
    *   Example plugin for Cloudflare ([cloudflare.py](app/plugins/custom_dns/cloudflare.py)).
*   **Database Management:**
    *   Uses a JSON file as a simple database.
    *   [DatabaseManager service](app/services/database_manager.py) handles CRUD operations.
*   **Configuration:**
    *   Uses a [config.py](app/config.py) file for application settings.
    *   Environment variables for sensitive information.
*   **Logging:**
    *   Configured logging to a file ([cn\_manager.log](app/.gitignore)).
*   **Virtual Environment:**
    *   Uses a virtual environment for dependency management.
*   **Nginx Installation and Configuration:**
    *   The [install.sh](install.sh) script automates the installation of Nginx and configures a basic Nginx configuration.

### Planned

*   **User Authentication and Authorization:**
    *   Implement user accounts and roles.
    *   Protect sensitive endpoints with authentication and authorization.
*   **Improved Nginx Configuration Management:**
    *   More robust Nginx configuration generation.
    *   Support for different Nginx configuration templates.
    *   Automated testing of Nginx configurations.
*   **Enhanced SSL Certificate Management:**
    *   Automated renewal of SSL certificates.
    *   Integration with different ACME clients.
    *   Support for wildcard certificates.
*   **DNS Record Management:**
    *   Automated DNS record creation and deletion for domain verification.
    *   Support for different DNS record types (A, CNAME, TXT, etc.).
*   **Web UI Improvements:**
    *   More user-friendly interface.
    *   Better error handling and feedback.
    *   AJAX for dynamic updates.
*   **API Endpoints:**
    *   Expose API endpoints for all features.
    *   Allow integration with other systems.
*   **Database Abstraction:**
    *   Support for different database backends (PostgreSQL, MySQL, etc.).
    *   Use an ORM for database interaction.
*   **Automated Testing:**
    *   Unit tests for all components.
    *   Integration tests for end-to-end functionality.
*   **Monitoring and Alerting:**
    *   Monitor the health of the application and Nginx.
    *   Send alerts on errors or performance issues.
*   **Proxy Rule Management:**
    *   Create, list, update, and delete proxy rules.
    *   [ProxyRule model](app/models/proxy_rule.py) defines the structure of a proxy rule.
*   **Location Management:**
    *   Create, list, update, and delete locations.
    *   [Location model](app/models/location.py) defines the structure of a location.

## Technologies Used

*   Python 3.11
*   Flask
*   Jinja2
*   Certbot
*   python-nginx
*   requests
*   dotenv

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd cn-manager
    ```

2.  Run the installation script:

    ```bash
    bash install.sh
    ```

    This script will:

    *   Update package lists.
    *   Install dependencies (Python 3, virtualenv, PostgreSQL, Nginx).
    *   Create a virtual environment.
    *   Install Python requirements from `app/requirements.txt`.
    *   Configure Nginx (basic example).
    *   Initialize PostgreSQL (basic example).

3.  Configure environment variables:

    *   Create a `.env` file in the `app/` directory.
    *   Add the following variables:

        ```
        CLOUDFLARE_TOKEN=<your_cloudflare_token>
        LETSENCRYPT_EMAIL=<your_email>
        PATH_TO_PROJ_CERT="/etc/nginx/proxy_manager/cert"
        ```

4.  Run the application:

    ```bash
    cd app
    source .venv/bin/activate
    python main.py
    ```

## Configuration

*   **config.py:** Contains application-wide configuration settings.
*   **.env:** Stores sensitive information like API keys and database credentials.
*   **Nginx Configuration:** Nginx configuration files are stored in `/etc/nginx/conf.d/`.

## Directory Structure

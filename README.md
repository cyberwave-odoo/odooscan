# Odoo Vulnerability Scanner

This project is a python 3 tool designed to scan Odoo instances for vulnerabilities, retrieve version information, and check the status of the database manager.

## Features
- Discover the version of an Odoo instance.
- Retrieve the list of databases available on the server.
- Check if the database manager is open or disabled.
- Authenticate with Odoo using a username and password.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/odoo-vulnerability-scanner.git
   ```
2. Navigate to the project directory:
   ```bash
   cd odoo-vulnerability-scanner
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the `odooscan.py` script with the desired options:
```bash
python odooscan.py --url http://localhost -p 8069 --check-db-manager -u admin -w admin_password
```

### Options
- `--url`: The full URL of the Odoo server (default: `http://localhost`).
- `-p`, `--port`: The port of the Odoo server (default: `8069`).
- `-dbm`, `--check-db-manager`: Check if the database manager is open.
- `-u`, `--user`: The username for authentication.
- `-w`, `--password`: The password for authentication.

## Example
To discover the version of an Odoo instance and check the database manager:
```bash
python odooscan.py --url http://example.com -p 8069 --check-db-manager
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request.

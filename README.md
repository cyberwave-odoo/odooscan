# Odoo Vulnerability Scanner

![Python](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-AGPL%20v3-blue)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen)

This project is a Python 3 tool designed to scan Odoo instances for vulnerabilities, retrieve version information, and check the status of the database manager.

## Features
- Discover the version of an Odoo instance.
- Retrieve the list of databases available on the server.
- Check if the database manager is open or disabled.
- Authenticate with Odoo using a username and password.
- Enumerate installed apps/modules.
- Test for demo data login activated using a predefined set of usernames and passwords.
- Fetch all users and their roles (requires admin credentials).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/cyberwave-odoo/odooscan.git
   ```
2. Navigate to the project directory:
   ```bash
   cd odooscan
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the `odooscan.py` script with the mandatory URL argument and optional parameters:
```bash
python odooscan.py http://example.com [options]
```

### Options
- `-p`, `--port`: The port of the Odoo server (default: `8069`).
- `-dbm`, `--check-db-manager`: Check if the database manager is open.
- `-u`, `--user`: The username for authentication.
- `-w`, `--password`: The password for authentication.
- `-lm`, `--list-modules`: Enumerate installed apps/modules.
- `-tdl`, `--test-demo-login`: Test if demo data login is activated using predefined credentials.
- `-fu`, `--fetch-users`: Fetch all users and their roles (requires admin credentials).

## Examples
To discover the version of an Odoo instance, check the database manager, and list installed modules:
```bash
python odooscan.py http://example.com --check-db-manager --list-modules
```

To test for demo data login:
```bash
python odooscan.py http://example.com --test-demo-login
```

To fetch all users and their roles:
```bash
python odooscan.py http://example.com -u admin -w admin --fetch-users
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request.

## License
This project is licensed under the AGPL v3 License. See the [LICENSE](LICENSE) file for details.ils.
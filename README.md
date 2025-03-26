# odooscan

`odooscan` is a command-line tool designed to help identify the version of an Odoo instance and optionally check if the database manager is open. This tool is useful for developers and security professionals working with Odoo.

## Features
- Discover the version of an Odoo instance.
- Check if the database manager is accessible.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/odooscan.git
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
Run the `odooscan` CLI tool with the following options:

```bash
python odooscan.py --url <Odoo URL> --port <Port> [--check-db-manager]
```

### Options
- `--url`: The full URL of the Odoo server (default: `http://localhost`).
- `--port`: The port of the Odoo server (default: `8069`).
- `--check-db-manager`: Check if the database manager is open (optional).

### Example
Discover the version of an Odoo instance running on `http://example.com`:
```bash
python odooscan.py --url http://example.com --port 8069
```

Check if the database manager is open:
```bash
python odooscan.py --url http://example.com --port 8069 --check-db-manager
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch.
4. Open a pull request.

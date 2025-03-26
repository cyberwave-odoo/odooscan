import click
from lib.core.logic import discover_version_logic

# Define the CLI command for discovering the Odoo version
@click.command()
@click.option('--url', default='http://localhost', required=True, help='The full URL of the Odoo server (e.g., http://localhost).')
@click.option('--port', default=8069, help='The Odoo server port (default: 8069).')
@click.option('--check-db-manager', is_flag=True, help='Check if the database manager is open.')
def discover_version(url, port, check_db_manager):
    """
    Discover the version of the Odoo instance and optionally check the database manager.

    Args:
        url (str): The URL of the Odoo server.
        port (int): The port of the Odoo server.
        check_db_manager (bool): Flag to check if the database manager is open.
    """
    # Call the logic function to perform the discovery
    discover_version_logic(url, port, check_db_manager)

# Entry point for the CLI tool
if __name__ == '__main__':
    discover_version()

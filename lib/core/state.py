import click
from lib.core.odoo_command import OdooCommand

class ScanState:
    _instance = None  # Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ScanState, cls).__new__(cls)
        return cls._instance

    @property
    def cli(self):
        return self._cli  # Getter for cli

    @cli.setter
    def cli(self, value):
        self._cli = value
        self.odooCommand = OdooCommand(value)  # Automatically update odooCommand

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self._cli = None  # Use private attribute for cli
            self.odooCommand = None  # Initialize as None
            self.version = None
            self.db_list = []
            self.demo_login_results = {}  # Store demo login test results
            self.initialized = True
            self.session = None

    def set_odoo_connection(self, odoo_connection):
        """Setter to store the Odoo connection object."""
        self.odoo_connection = odoo_connection

    def discover_db_version(self):
        try:
            # Use the existing CliCommand object
            self.session = self.odooCommand.connect_to_odoo()
            self.set_odoo_connection(self.session)  # Store the connection
            version_info = self.session.version  # This returns a dictionary or string

            # Attempt to retrieve the database list
            db_list = []
            try:
                db_list = self.session.db.list()
            except Exception as e:
                click.echo(f"Warning: Unable to retrieve database list. Error: {e}")

            
            self.version=version_info
            self.db_list=db_list
            click.echo(f"Odoo Version: {self.version} and database list: {self.db_list}")
            return self

        except Exception as e:
            click.echo(f"Error: {e}")
            raise e

# Provide a global access point for the singleton instance
def get_scan_state():
    return ScanState()


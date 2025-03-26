from lib.core.odoo_info import OdooInfo
import click

class ScanState:
    def __init__(self, odooCommand):
        self.odooCommand = odooCommand

    def set_odoo_connection(self, odoo_connection):
        """Setter to store the Odoo connection object."""
        self.odoo_connection = odoo_connection

    def discover_db_version(self):
        try:
            # Use the existing OdooCommand object
            odoo = self.odooCommand.connect_to_odoo()
            self.set_odoo_connection(odoo)  # Store the connection
            version_info = odoo.version  # This returns a dictionary or string

            # Attempt to retrieve the database list
            db_list = []
            try:
                db_list = odoo.db.list()
            except Exception as e:
                click.echo(f"Warning: Unable to retrieve database list. Error: {e}")

            # Create OdooInfo object
            info = OdooInfo(version=version_info, db_list=db_list)
            click.echo(f"Odoo Version: {info.version} and database list: {info.db_list}")

            return info

        except Exception as e:
            click.echo(f"Error: {e}")
            raise e


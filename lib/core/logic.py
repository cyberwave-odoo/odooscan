import os
import json
from lib.odoo_utils import check_database_manager
from lib.core.odoo_command import OdooCommand
from lib.core.odoo_info import OdooInfo
import click
from lib.settings.path import DATA_FOLDER
def discover_version_logic(url, port, check_db_manager):
    try:
        # Create OdooCommand object
        command = OdooCommand(url=url, port=port, check_db_manager=check_db_manager)

        # Connect to the Odoo server
        odoo = command.connect_to_odoo()
        version_info = odoo.version  # This returns a dictionary or string

        # Create OdooInfo object
        info = OdooInfo(version=version_info)

        click.echo(f"Odoo Version: {info.version}")

        # Check the database manager if the option is enabled
        if command.check_db_manager:
            # Save version-specific data
            
            versions_file = os.path.join(DATA_FOLDER, 'urls', 'db_manager.json')
            with open(versions_file, 'r') as f:
                db_manager_urls = json.load(f)

            db_manager_url_template = db_manager_urls.get(info.version, db_manager_urls.get("default"))
            db_manager_url = db_manager_url_template.format(protocol=command.protocol, host=command.host, port=command.port)
            check_database_manager(db_manager_url)

    except Exception as e:
        click.echo(f"Error: {e}")

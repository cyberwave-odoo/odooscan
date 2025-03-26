import os
import json
from lib.settings.path import DATA_FOLDER
import click
import requests

def check_database_manager(db_manager_url):
    """
    Check if the database manager is open or disabled.
    """
    try:
        response = requests.get(db_manager_url)
        if response.status_code == 200:
            if "The database manager has been disabled by the administrator" in response.text:
                click.echo("Database Manager is disabled by the administrator.")
            else:
                click.echo(click.style(f"Database Manager is likely open at {db_manager_url}", fg="green"))
        else:
            click.echo(f"Database Manager is not accessible. HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        click.echo(f"Error checking Database Manager: {e}")
        raise e

def handle_db_manager_check(command, version):
    """
    Handle the logic for checking the database manager.
    """
    versions_file = os.path.join(DATA_FOLDER, 'urls', 'db_manager.json')
    with open(versions_file, 'r') as f:
        db_manager_urls = json.load(f)

    db_manager_url_template = db_manager_urls.get(version, db_manager_urls.get("default"))
    db_manager_url = db_manager_url_template.format(protocol=command.protocol, host=command.host, port=command.port)
    check_database_manager(db_manager_url)


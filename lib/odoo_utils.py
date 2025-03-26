import requests
import click

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
                click.echo("Database Manager is likely open.")
        else:
            click.echo(f"Database Manager is not accessible. HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        click.echo(f"Error checking Database Manager: {e}")
        raise e

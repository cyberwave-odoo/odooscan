from lib.option.common_lib import *


def check_database_manager(db_manager_url):
    """
    Check if the database manager is open or disabled.
    This works because the response.text is not translated in the Odoo interface.
    """
    try:
        response = requests.get(db_manager_url)
        if response.status_code == 200:
            if "The database manager has been disabled by the administrator" in response.text:
                logger.log("Database Manager is disabled by the administrator.")
            else:
                logger.log(click.style(f"Database Manager is likely open at {db_manager_url}", fg="green"))
        else:
            logger.log(click.style(f"Database Manager is not accessible. HTTP Status: {response.status_code}", fg="red"))
    except requests.RequestException as e:
        click.echo(click.style(f"Error checking Database Manager: {e}", fg="red"))
        raise e

def handle_db_manager_check(version):
    """
    Handle the logic for checking the database manager.
    """
    versions_file = os.path.join(DATA_FOLDER, 'urls', 'db_manager.json')
    with open(versions_file, 'r') as f:
        db_manager_urls = json.load(f)

    db_manager_url_template = db_manager_urls.get(version, db_manager_urls.get("default"))
    db_manager_url = db_manager_url_template.format(protocol=state._cli.protocol, host=state._cli.host, port=state._cli.port)
    logger.verbose(click.style(f"Checking database manager at {db_manager_url}...", fg="blue"))
    check_database_manager(db_manager_url)


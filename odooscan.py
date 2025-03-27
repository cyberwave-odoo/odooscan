import click
from lib.core.state import ScanState
from lib.core.odoo_command import OdooCommand
from lib.option.db_manager import handle_db_manager_check
from lib.option.enumerate_modules import enumerate_installed_modules
from lib.option.test_demo_login import test_demo
from lib.logging.logger import Logger


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument('url')
@click.option('-p', '--port', default=8069, help='The Odoo server port (default: 8069).', show_default=True)
@click.option('-dbm', '--check-db-manager', is_flag=True, help='Check if the database manager is open.')
@click.option('-u', '--user', help='The username for authentication.')
@click.option('-w', '--password', help='The password for authentication.')
@click.option('-lm', '--list-modules', is_flag=True, help='List installed apps/modules.')
@click.option('-tdl', '--test-demo-login', is_flag=True, help='Enumerate demo users default user:pwd.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
def start_scan(url, port, check_db_manager, user, password, list_modules, test_demo_login, verbose):

    logger = Logger(verbose)

    logger.log(click.style(f"Starting scan on {url}:{port}...", fg="blue"))
    command = OdooCommand(url, port, check_db_manager, user=user, password=password, list_modules=list_modules, test_demo_login=test_demo_login)
    scan = ScanState(command)
    
    info = scan.discover_db_version()
    
    # Check the database manager if the option is enabled
    if command.check_db_manager:
        handle_db_manager_check(command, info.version)
    
    # Handle multiple databases
    if hasattr(info, 'db_list') and len(info.db_list) > 1:
        logger.log("Multiple databases detected:")
        for i, db in enumerate(info.db_list, start=1):
            logger.log(f"{i}. {db}")
        db_index = click.prompt(click.style("Select the database by number (default: 1)", fg="blue"), type=int, default=1)
        selected_db = info.db_list[db_index - 1]
        logger.log(f"Database Selected: {selected_db}")
        command.set_dbname(selected_db)
    elif hasattr(info, 'db_list') and len(info.db_list) == 1:
        command.set_dbname(info.db_list[0])

    if user is not None and password is not None:
        command.login_to_odoo(scan.odoo_connection)

    # Enumerate installed modules if the option is enabled
    if list_modules:
        enumerate_installed_modules(command, info.version)
    if test_demo_login:
        test_demo(command, info)

    logger.log("Scan completed.")

if __name__ == '__main__':
    start_scan()

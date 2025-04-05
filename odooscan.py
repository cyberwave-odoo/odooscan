import click
from lib.core.state import ScanState
from lib.core.odoo_command import OdooCommand
from lib.option.db_manager import handle_db_manager_check
from lib.option.enumerate_modules import enumerate_installed_modules
from lib.option.test_demo_login import test_demo
from lib.logging.logger import Logger
from lib.option.fetch_users import fetch_users_and_roles

# Singleton instance for the OdooCommand
command = None

def setup_logger(verbose):
    """Initialize and return logger."""
    return Logger(verbose)

def initialize_command_singleton(url, port, check_db_manager, user, password, list_modules, test_demo_login):
    """Initialize or return the singleton OdooCommand object."""
    global command
    if command is None:
        command = OdooCommand(
            url, 
            port, 
            check_db_manager, 
            user=user, 
            password=password,
            list_modules=list_modules, 
            test_demo_login=test_demo_login
        )
    return command

def perform_scan(command, logger):
    """Perform the scanning operation and return scan info."""
    scan = ScanState(command)
    info = scan.discover_db_version()
    return scan, info

def check_db_manager_if_enabled(command, info_version, logger):
    """Check the database manager if the option is enabled."""
    if command.check_db_manager:
        logger.log("Checking database manager...")
        handle_db_manager_check(command, info_version)

def select_database(info, command, logger):
    """Handle database selection."""
    if hasattr(info, 'db_list'):
        if len(info.db_list) > 1:
            logger.log("Multiple databases detected:")
            for i, db in enumerate(info.db_list, start=1):
                logger.log(f"{i}. {db}")
            db_index = click.prompt(click.style("Select the database by number (default: 1)", fg="blue"), type=int, default=1)
            selected_db = info.db_list[db_index - 1]
            logger.log(f"Database Selected: {selected_db}")
            command.set_dbname(selected_db)
        elif len(info.db_list) == 1:
            selected_db = info.db_list[0]
            logger.log(f"Using database: {selected_db}")
            command.set_dbname(selected_db)

def login_if_credentials_provided(command, scan, user, password, logger):
    """Login to Odoo if credentials are provided."""
    if user is not None and password is not None:
        logger.log("Attempting to login with provided credentials...")
        command.login_to_odoo(scan.odoo_connection)

def handle_operations(command, info, list_modules, test_demo_login, fetch_users, user, password, logger):
    """Handle Odoo operations based on provided options."""
    if list_modules:
        logger.log("Enumerating installed modules...")
        enumerate_installed_modules(command, info.version)
    
    if test_demo_login:
        logger.log("Testing demo login credentials...")
        test_demo(command, info)
    
    if fetch_users:
        if not user or not password:
            logger.log(click.style("Error: Admin username and password are required for fetching users.", fg="red"))
            return False
        logger.log("Fetching users and roles...")
        fetch_users_and_roles(command)
    
    return True

def validate_fetch_users(ctx, param, value):
    """Callback to request username and password if --fetch-users is enabled."""
    if value:
        if not ctx.params.get('user') or not ctx.params.get('password'):
            raise click.BadParameter('--fetch-users requires both --user and --password')
    return value

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument('url')
@click.option('-p', '--port', default=8069, help='The Odoo server port (default: 8069).', show_default=True)
@click.option('-dbm', '--check-db-manager', is_flag=True, help='Check if the database manager is open.')
@click.option('-u', '--user', help='The username for authentication.')
@click.option('-w', '--password', help='The password for authentication.')
@click.option('-lm', '--list-modules', is_flag=True, help='List installed apps/modules.')
@click.option('-tdl', '--test-demo-login', is_flag=True, help='Enumerate demo users default user:pwd.')
@click.option('-fu', '--fetch-users', is_flag=True, callback=validate_fetch_users, expose_value=True, help='Fetch all users and their roles (requires admin credentials).')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
def start_scan(url, port, check_db_manager, user, password, list_modules, test_demo_login, fetch_users, verbose):
    """Start an Odoo server scan with the specified options."""
    # Setup
    logger = setup_logger(verbose)
    logger.log(click.style(f"Starting scan on {url}:{port}...", fg="blue"))
    
    # Initialize command singleton and perform scan
    global command
    command = initialize_command_singleton(url, port, check_db_manager, user, password, list_modules, test_demo_login)
    scan, info = perform_scan(command, logger)
    
    # Check database manager
    check_db_manager_if_enabled(command, info.version, logger)
    
    # Handle database selection
    select_database(info, command, logger)
    
    # Login if credentials provided
    login_if_credentials_provided(command, scan, command.user, command.password, logger)
    
    # Handle operations
    if handle_operations(command, info, list_modules, test_demo_login, fetch_users, command.user, command.password, logger):
        logger.log(click.style("Scan completed successfully.", fg="green"))
    else:
        logger.log(click.style("Scan completed with errors.", fg="yellow"))

if __name__ == '__main__':
    start_scan()

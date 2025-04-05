import click
from lib.core.state import ScanState
from lib.core.odoo_command import CliCommand, OdooCommand
from lib.option.db_manager import handle_db_manager_check
from lib.option.enumerate_modules import enumerate_installed_modules
from lib.option.test_demo_login import test_demo
from lib.logging.logger import Logger
from lib.option.fetch_users import fetch_users_and_roles
from lib.core.state import get_scan_state
# Define a global variable for the CliCommand instance

state = get_scan_state()
cli_command = None
logger = None
def setup_logger(verbose):
    """Initialize and return logger."""
    return Logger(verbose)

def initialize_command_singleton(**kwargs):
    """Initialize or return the singleton OdooCommand object."""
    cli = CliCommand(**kwargs)
    return cli

def perform_scan(state):
    """Perform the scanning operation and return scan info."""
    state = state.discover_db_version()
    return state

def check_db_manager_if_enabled(info_version):
    """Check the database manager if the option is enabled."""
    if cli_command.check_db_manager:
        logger.log("Checking database manager...")
        handle_db_manager_check(info_version)

def select_database():
    info = state
    """Handle database selection."""
    if hasattr(info, 'db_list'):
        if len(info.db_list) > 1:
            logger.log("Multiple databases detected:")
            for i, db in enumerate(info.db_list, start=1):
                logger.log(f"{i}. {db}")
            db_index = click.prompt(click.style("Select the database by number (default: 1)", fg="blue"), type=int, default=1)
            selected_db = info.db_list[db_index - 1]
            logger.log(f"Database Selected: {selected_db}")
            cli_command.set_dbname(selected_db)
        elif len(info.db_list) == 1:
            selected_db = info.db_list[0]
            logger.log(f"Using database: {selected_db}")
            cli_command.set_dbname(selected_db)

def login_if_credentials_provided():
    """Login to Odoo if credentials are provided."""
    if state.odooCommand.user is not None and state.odooCommand.password is not None:
        logger.log("Attempting to login with provided credentials...")
        state.odooCommand.login_to_odoo(state.session)

def handle_operations(state, list_modules, test_demo_login, fetch_users):
    """Handle Odoo operations based on provided options."""
    if list_modules:
        logger.log("Enumerating installed modules...")
        enumerate_installed_modules(state)
    
    if test_demo_login:
        logger.log("Testing demo login credentials...")
        test_demo(state)
    
    if fetch_users:
        if not state._cli.user or not state._cli.password:
            logger.log(click.style("Error: Admin username and password are required for fetching users.", fg="red"))
            return False
        logger.log("Fetching users and roles...")
        fetch_users_and_roles(state)
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
def start_scan(**kwargs):
    """Start an Odoo server scan with the specified options."""
    global cli_command  # Declare the global variable
    global logger  # Declare the global variable
    global state  # Declare the global variable
    # Setup
    logger = setup_logger(kwargs.get('verbose'))
    logger.log(click.style(f"Starting scan on {kwargs.get('url')}:{kwargs.get('port')}...", fg="blue"))
    
    # Initialize command singleton and assign to the global variable
    cli_command = initialize_command_singleton(**kwargs)
    state.cli = cli_command
    state = perform_scan(state)
    
    # Check database manager
    check_db_manager_if_enabled(state.version)
    
    # Handle database selection
    select_database()
    
    # Login if credentials provided
    login_if_credentials_provided()
    
    # Handle operations
    if handle_operations(state, kwargs.get('list_modules'), kwargs.get('test_demo_login'), kwargs.get('fetch_users')):
        logger.log(click.style("Scan completed successfully.", fg="green"))
    else:
        logger.log(click.style("Scan completed with errors.", fg="yellow"))

if __name__ == '__main__':
    start_scan()

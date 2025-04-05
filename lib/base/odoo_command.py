import odoorpc
from urllib.parse import urlparse
from lib.logging.logger import Logger
logger = Logger()

class CliCommand:
    """
    Represents a command to interact with an Odoo instance.
    """
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CliCommand, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        if not hasattr(self, '_initialized'):  # Ensure __init__ runs only once
            self.url = kwargs.get('url')
            parsed_url = urlparse(self.url)
            self.protocol = parsed_url.scheme
            self.host = parsed_url.hostname
            self.port = kwargs.get('port')
            self.protocol_map = {"https": 'jsonrpc+ssl', "http": "jsonrpc"}
            
            self.check_db_manager = kwargs.get('check_db_manager', False)
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.dbname = kwargs.get('dbname')
            self.test_demo_login = kwargs.get('test_demo_login', False)
            self.list_modules = kwargs.get('list_modules', False)
            self.fetch_users = kwargs.get('fetch_users', False)
            self._initialized = True  # Mark as initialized

    # Getter and Setter for protocol
    def get_protocol(self):
        return self.protocol

    def set_protocol(self, protocol):
        self.protocol = protocol

    # Getter and Setter for host
    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host

    # Getter and Setter for port
    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    # Getter and Setter for check_db_manager
    def get_check_db_manager(self):
        return self.check_db_manager

    def set_check_db_manager(self, check_db_manager):
        self.check_db_manager = check_db_manager

    # Getter and Setter for user
    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    # Getter and Setter for password
    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    # Getter and Setter for dbname
    def get_dbname(self):
        return self.dbname

    def set_dbname(self, dbname):
        self.dbname = dbname


class OdooCommand():
    """
    Extends CliCommand to provide specific functionality for interacting with Odoo.
    """
    def __init__(self, cli_command=None, **kwargs):
        if cli_command:
            self.cli = cli_command
            self.user = cli_command.get_user()
            self.password = cli_command.get_password()
        

    def connect_to_odoo(self):
        logger.verbose(f"Connecting to Odoo at {self.cli.protocol}://{self.cli.host}:{self.cli.port}")
        odoo = odoorpc.ODOO(self.cli.host, protocol=self.cli.protocol_map[self.cli.protocol], port=self.cli.port)
        return odoo
    
    def login_to_odoo(self, odoo):
        if self.user and self.password and self.cli.dbname:
            logger.verbose(f"Logging in as {self.user} to {self.cli.dbname}")
            odoo.login(self.cli.dbname, self.user, self.password)
        else:
            logger.log(f"No user, password, or dbname set for login attempt with user {self.user}")
        return odoo

    def copy(self):
        """
        Create a copy of the current OdooCommand instance.
        """
        attributes = vars(self).copy()  # Get all instance attributes as a dictionary
        attributes['url'] = f"{self.cli.protocol}://{self.cli.host}"  # Reconstruct the URL
        return OdooCommand(**attributes)

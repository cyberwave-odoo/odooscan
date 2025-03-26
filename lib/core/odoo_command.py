import odoorpc
from urllib.parse import urlparse
import click

class OdooCommand:
    """
    Represents a command to interact with an Odoo instance.
    """
    
    def __init__(self, url, port, check_db_manager, user=None, password=None, dbname=None):
        parsed_url = urlparse(url)
        self.protocol = parsed_url.scheme
        self.host = parsed_url.hostname
        self.port = port
        self.protocol_map = {"https": 'jsonrpc+ssl', "http" : "jsonrpc"}
        
        self.check_db_manager = check_db_manager
        self.user = user
        self.password = password
        self.dbname = dbname

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

    def connect_to_odoo(self):
        odoo = odoorpc.ODOO(self.host, protocol=self.protocol_map[self.protocol], port=self.port)
        return odoo
    
    def login_to_odoo(self, odoo):
        if self.user and self.password and self.dbname:
            click.echo(f"Logging in as {self.user} to {self.dbname}")
            odoo.login(self.dbname, self.user, self.password)
        return odoo
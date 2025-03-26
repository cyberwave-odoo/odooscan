import odoorpc
from urllib.parse import urlparse

class OdooCommand:
    """
    Represents a command to interact with an Odoo instance.
    """
    
    def __init__(self, url, port, check_db_manager):
        parsed_url = urlparse(url)
        self.protocol = parsed_url.scheme
        self.host = parsed_url.hostname
        self.port = port
        self.protocol_map = {"https": 'jsonrpc+ssl', "http" : "jsonrpc"}
        
        self.check_db_manager = check_db_manager

    def connect_to_odoo(self):
        return odoorpc.ODOO(self.host,protocol=self.protocol_map[self.protocol], port=self.port)
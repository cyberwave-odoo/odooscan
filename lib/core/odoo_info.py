class OdooInfo:
    """
    Represents the gathered information about the Odoo instance.
    """
    def __init__(self, version, db_list=[]):
        self.version = version
        self.db_list = db_list
        self.demo_login_results = {}  # Store demo login test results

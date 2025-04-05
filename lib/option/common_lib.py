import os
import json
from lib.settings.path import DATA_FOLDER
import click
import requests
from lib.logging.logger import Logger
from lib.core.odoo_command import CliCommand
from lib.core.state import get_scan_state
state = get_scan_state()
logger = Logger()

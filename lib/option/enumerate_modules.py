from lib.option.common_lib import *
from bs4 import BeautifulSoup  # Add this import


def enumerate_installed_modules(state):
    """
    Enumerate installed apps/modules from the Odoo instance.
    """
    versions_file = os.path.join(DATA_FOLDER, 'urls', 'enumerate_modules.json')
    with open(versions_file, 'r') as f:
        modules_urls = json.load(f)

    modules_url_template = modules_urls.get(state.version, modules_urls.get("default"))
    modules_url = modules_url_template.format(protocol=state._cli.protocol, host=state._cli.host, port=state._cli.port)

    try:
        logger.verbose(click.style(f"Fetching modules from {modules_url}", fg="blue"))
        response = requests.get(modules_url)
        if response.status_code == 200:
            logger.verbose(click.style("Parsing module data...", fg="blue"))
            # Parse HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract module names and explanations from <dl> tags
            modules = [
                {
                    "name": dl.find('a').text.strip(),
                    "description": dl.find('dd').text.strip() if dl.find('dd') else "No description available"
                }
                for dl in soup.find_all('dl', class_='dl-horizontal')
                if dl.find('a')
            ]
            if modules:
                logger.log(click.style("Installed Modules (from HTML):", fg="green"))
                for module in modules:
                    logger.log(f"- {module['name']}: {module['description']}")
            else:
                logger.log(click.style("No modules found or insufficient permissions in HTML response.", fg="yellow"))
            
        else:
            logger.log(click.style(f"Failed to fetch modules. HTTP Status: {response.status_code}", fg="red"))
    except requests.RequestException as e:
        logger.log(click.style(f"Error enumerating installed modules: {e}", fg="red"))
        raise e


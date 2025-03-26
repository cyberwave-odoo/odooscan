from lib.option.common_lib import *
from bs4 import BeautifulSoup  # Add this import

def enumerate_installed_modules(command, version):
    """
    Enumerate installed apps/modules from the Odoo instance.
    """
    versions_file = os.path.join(DATA_FOLDER, 'urls', 'enumerate_modules.json')
    with open(versions_file, 'r') as f:
        modules_urls = json.load(f)

    modules_url_template = modules_urls.get(version, modules_urls.get("default"))
    modules_url = modules_url_template.format(protocol=command.protocol, host=command.host, port=command.port)

    try:
        response = requests.get(modules_url)
        if response.status_code == 200:
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
                click.echo("Installed Modules (from HTML):")
                for module in modules:
                    click.echo(f"- {module['name']}: {module['description']}")
            else:
                click.echo("No modules found or insufficient permissions in HTML response.")
            
        else:
            click.echo(f"Failed to fetch modules. HTTP Status: {response.status_code}")
    except requests.RequestException as e:
        click.echo(f"Error enumerating installed modules: {e}")
        raise e


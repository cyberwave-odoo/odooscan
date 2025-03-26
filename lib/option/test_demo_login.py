from lib.option.common_lib import *
from lib.core.odoo_command import OdooCommand

def test_demo(command, info):
    """
    Test if demo data login is activated using predefined credentials.
    """
    demo_users_file = os.path.join(DATA_FOLDER, 'userenum', 'demo_users.json')
    with open(demo_users_file, 'r') as f:
        demo_users = json.load(f)

    credentials = demo_users.get(info.version, demo_users.get("default"))

    for user in credentials:
        try:
            odoo_command = command.copy()
            odoo_command.user = user["username"]
            odoo_command.password = user["password"]
            odoo = odoo_command.connect_to_odoo()
            odoo_command.login_to_odoo(odoo)
            
            # Check if the login was successful by verifying the uid attribute
            if odoo.env.uid:
                click.echo(click.style(f"Demo login successful: {user['username']} / {user['password']}", fg="green"))
            else:
                click.echo(f"Failed login attempt: {user['username']} / {user['password']}")
        except Exception as e:
            click.echo(f"Error testing demo login for {user['username']}: {e}")

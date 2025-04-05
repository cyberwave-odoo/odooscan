from lib.option.common_lib import *


def test_demo():
    """
    Test if demo data login is activated using predefined credentials.
    """
      # Get the global logger instance
    logger.verbose(click.style(f"Testing demo login demo users", fg="blue"))
    demo_users_file = os.path.join(DATA_FOLDER, 'userenum', 'demo_users.json')
    with open(demo_users_file, 'r') as f:
        demo_users = json.load(f)

    credentials = demo_users.get(state.version, demo_users.get("default"))

    for user in credentials:
        try:
            odoo_command = state.odooCommand
            odoo_command.user = user["username"]
            odoo_command.password = user["password"]
            odoo = odoo_command.connect_to_odoo()
            odoo_command.login_to_odoo(odoo)
            
            # Check if the login was successful by verifying the uid attribute
            if odoo.env.uid:
                logger.log(click.style(f"Demo login successful: {user['username']} / {user['password']}", fg="green"))
            else:
                logger.log(click.style(f"Failed login attempt: {user['username']} / {user['password']}", fg="red"))
        except Exception as e:
            logger.log(click.style(f"Error testing demo login for {user['username']}: {e}", fg="red"))
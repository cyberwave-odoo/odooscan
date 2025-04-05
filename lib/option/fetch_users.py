from lib.option.common_lib import *
import polars as pl

def fetch_users_and_roles(command):
    """
    Fetch all users and their roles from the Odoo instance.
    """
    try:
        odoo = command.connect_to_odoo()
        command.login_to_odoo(odoo)  # Login using admin credentials

        logger.verbose("Fetching users and their roles...")
        users = odoo.env['res.users'].search_read([], ['id', 'name', 'login', 'groups_id'])
        pl_users = pl.DataFrame(users)
        logger.log(pl_users)

        groups = odoo.env['res.groups'].search_read([], ['id', 'name'])
        pl_groups = pl.DataFrame(groups)

        # Pivot longer on groups_id
        pl_users_long = pl_users.explode('groups_id')

        # Join with groups DataFrame
        user_groups_joined = pl_users_long.join(pl_groups, left_on='groups_id', right_on='id', how='left')

        # Pivot wider to have one line per user with all their groups
        user_groups_wide = user_groups_joined.group_by(['id', 'name', 'login']).agg(
            pl.col('name_right').alias('groups')
        )
        logger.log(user_groups_wide)
        logger.log(click.style("Users and roles fetched successfully.", fg="green"))
        
    except Exception as e:
        logger.log(click.style(f"Error fetching users and roles: {e}", fg="red"))

# list users
# list fields of
import odoorpc
import polars as pl
# Connect to the Odoo server
odoo = odoorpc.ODOO('localhost', port=8069)  # Replace with your server URL and port
print("rpc")
# Log in to the database
odoo.login('odoo-db', 'piborlee@epfc.eu', 'test')  # Replace with your credentials
#odoo.login('odoo-db', '2909mabauweleers@student.epfc.eu', 'test')  # Replace with your credentials
print('logged')
# Access the model (e.g., res.partner)
model = odoo.env['res.users']
print('env')
# Define the domain and fields


# Perform the search_read call
#polars = model.search_read([], fields=['login','oauth_access_token'])
#df = pl.DataFrame(polars)
#print(df)

# List the fields of the model
#fields = model.fields_get()
#print("Fields in model:", fields.keys())


# List all available functions on the model
# You can check if a module is installed this way
#methods = dir(odoo.env['ir.cron'])
#df = pl.DataFrame(methods)
#print(df)

toto = model.USER_PRIVATE_FIELDS
print(dir(toto))
print(type(toto))


# Append 'oauth_access_token' to USER_PRIVATE_FIELDS via RPC


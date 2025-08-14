import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

import psycopg2

# conn = psycopg2.connect("host=db.myapp.com dbname=my_app user=postgres password=secret")


# # Example server function using external DB
# @anvil.server.callable
# def get_user_signups():
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT COUNT(*), DATE_TRUNC('week', signup_date) AS d
#              FROM users
#              WHERE signup_date > NOW() - INTERVAL '3 months'
#              GROUP BY DATE_TRUNC('week', signup_date)
#              ORDER BY d;
#     """)
#     return list(cur)

import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from pydantic import BaseModel


def say_hello():
    print("Hello, world")

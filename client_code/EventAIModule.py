import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from pydantic import BaseModel


class EventAISchema(BaseModel):

    class Themes(BaseModel):
        theme: str

def say_hello():
    print("Hello, world")

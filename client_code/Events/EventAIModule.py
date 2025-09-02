import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from pydantic import BaseModel


class EventAISchema(BaseModel):

    class Theme(BaseModel):
        theme: str
        description: str
        colors: str
        decor_ideas: str

    themes: list[Theme]

    class Menu(BaseModel):
        type: str
        description: str
        options: list[str]
        bev_suggestions: str
        budget_allocation: str

    menus: list[Menu]
    
def say_hello():
    print("Hello, world")

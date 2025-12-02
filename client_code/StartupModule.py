import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
import anvil.users
from . import Events
from . import Tasks


def startup():
    # user = anvil.users.login_with_form()
    # if not user['color']:
    #     anvil.server.call('add_user_color')

    # open_form("Events.EventList")
    # open_form("Events.EventAI")
    open_form("Events.EventForm")
    # open_form("Events.EventView")
    # open_form("Events.EventAIModule")
    # open_form("Tasks.TaskForm")


startup()

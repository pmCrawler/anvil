import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
from .Events.EventList import EventList


def startup():
    # user = anvil.users.login_with_form()
    # if not user['color']:
    #     anvil.server.call('add_user_color')
    # open_form("EventList")
    open_form("EventList")


startup()

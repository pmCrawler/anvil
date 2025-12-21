from ._anvil_designer import EventCardTemplateTemplate
from anvil import *
import m3.components as m3
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EventCardTemplate(EventCardTemplateTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # self.event_id = anvil.server.call("get_event", properties["item"]["id"])
        # print(f"Event Id: {self.event_id}")

    def btn_details_click(self, **event_args):
        """This method is called when the component is clicked."""
        event = self.item
        print(f"ID: {event['id']}")
        open_form("Events.EventView", **event)
        #  ("EventView", self.item)

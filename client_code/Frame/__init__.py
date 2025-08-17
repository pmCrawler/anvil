from ._anvil_designer import FrameTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import m3.components as m3
from ..Events.EventList import EventList


class Frame(FrameTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def nav_link_events_click(self, **event_args):
        """This method is called when the component is clicked"""
        open_form("EventList")
        pass

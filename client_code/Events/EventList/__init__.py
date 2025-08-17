from ._anvil_designer import EventListTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EventCardTemplate import EventCardTemplate


class EventList(EventListTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.events = anvil.server.call("get_events")
        self.repeating_panel_1.items = self.events

from ._anvil_designer import EventListTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EventCardTemplate import EventCardTemplate
import anvil.http


inputs = {
    "Event Title": "sample event",
    "Type": "book club",
    "Date": "4/4/2026",
    "Guest Count": 30,
    "Venue Type": "club house",
    "Food and Beverage": True,
    "Event Setting": "indoor",
    "Extra Info": "hosting my first book club event",
}


class EventList(EventListTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # resp = anvil.server.call("get_event_data", inputs)
        # print(resp)
        resp = anvil.http.request(
            "http://localhost:5678/webhook/dafb4274-ddf0-4874-a0e1-5a362c525170",
            data=inputs,
            json=True,
        )
        print(resp)

        self.events = anvil.server.call("get_events")
        self.repeating_panel_1.items = self.events

    def btn_new_event_click(self, **event_args):
        """This method is called when the component is clicked."""
        open_form("Events.EventForm")

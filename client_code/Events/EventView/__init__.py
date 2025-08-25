from ._anvil_designer import EventViewTemplate
from anvil import *
import anvil.users
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json


class EventView(EventViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.item = properties
        self.title_heading.text = self.item["event_title"]
        # self.txt_date.text = self.item["event_date"]
        print(f"Event Title: {self.item['event_title']}")

        # self.card_content_container_1.add_component(self.heading_1)
        pass

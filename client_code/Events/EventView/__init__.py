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
    def __init__(self, event_id=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        event = anvil.server.call('get_event')
        print(event.get_id())


        self.lbl_info = Label(
            text="The Morrison Residence\n456 Oak Avenue\nPortland, OR 97204"
        )
        marker = GoogleMap.Marker(
            animation=GoogleMap.Animation.DROP,
            position=GoogleMap.LatLng(45.5152, -122.6784),
            title=self.lbl_info.text,
            visible=True,
        )
        self.google_map_1.center = marker.position
        self.google_map_1.height = "150"
        self.google_map_1.zoom = 15

        self.google_map_1.add_component(marker)
        self.item = properties
        self.title_heading.text = "Liverpool watch party"

        pass

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

        map = GoogleMap()
        green_icon = GoogleMap.Icon(
            url="http://maps.google.com/mapfiles/kml/paddle/grn-blank.png",
            size="10",
            scaled_size="18",
        )
        marker = GoogleMap.Marker(
            animation=GoogleMap.Animation.DROP,
            icon=green_icon,
            position=GoogleMap.LatLng(52.2053, 0.1218),
            title="The Morrison Residence",
            # label="The Morrison Residence",
            visible=True,
        )
        map.center = marker.position
        map.height = "350"
        map.margin = "16"
        map.zoom = 15

        map.add_component(marker)
        self.content_panel.add_component(map)
        # map.center = GoogleMap.LatLng(45.5152, -122.6784)
        # map.zoom = 13
        # map.disable_default_ui = True
        # map.map_data = {
        #     "address": "456 Oak Avenue, Portland, OR 97204",
        #     "venue_name": "The Morrison Residence",
        #     "coordinates": {"lat": 45.5152, "lng": -122.6784},
        # }

        # self.google_map_1.add_component(map)

        self.item = properties
        self.title_heading.text = "Liverpool watch party"  # self.item["event_title"]
        # self.txt_date.text = self.item["event_date"]
        # print(f"Event Title: {self.item['event_title']}")

        # self.card_content_container_1.add_component(self.heading_1)
        pass

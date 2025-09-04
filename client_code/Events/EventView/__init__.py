from ._anvil_designer import EventViewTemplate
from anvil import *
import anvil.users
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import date


class EventView(EventViewTemplate):
    def __init__(self, event_id=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # [996976,4270964888]
        # FOR TESTING ONLY
        event_id = 4270964888
        event = anvil.server.call("get_event_by_id", event_id)

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
        self.heading_title.text = event["title"]

        self.grid_event_data.background = "theme:Surface Variant"
        self.grid_event_data.add_component(
            Label(
                text="Description:",
                bold=True,
                font_size=12,
            ),
            row="row1",
            col_xs=0,
            width_xs=1,
        )

        self.grid_event_data.add_component(
            Label(text=event["description"], font_size=12),
            row="row1",
            col_xs=2,
            width_xs=2,
        )

        self.grid_event_data.add_component(
            Label(text="Date:", bold=True, font_size=12),
            row="row1",
            col_xs=5,
            width_xs=1,
        )

        self.grid_event_data.add_component(
            Label(text=event["event_datetime"], font_size=12),
            row="row1",
            col_xs=6,
            width_xs=2,
        )

        self.grid_event_data.add_component(
            Button(text="Submit"), row="row2", col_xs=3, width_xs=2
        )

        # self.grid_event_data

        pass

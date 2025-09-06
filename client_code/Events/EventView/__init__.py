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
from collections import OrderedDict


class EventView(EventViewTemplate):
    def __init__(self, event_id=4270964888, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        lst_keys = [
            "event_datetime",
            "event_setting",
            "budget",
            "guest_count",
            "location",
        ]

        event = anvil.server.call("get_event_by_id", event_id)

        self.cpanel_main.col_spacing = "none"
        self.grid_panel = GridPanel(spacing_above="None", spacing_below="None")

        self.heading_title.text = event["title"]
        self.txt_description.text = event["description"]

        row, col = 0, 0

        key_vals = OrderedDict((k, event[k]) for k in lst_keys if k in event)

        for k, v in key_vals.items():
            lbl_key = m3.Text(
                text=k.title().replace("_", " "),
                bold=True,
                font_size=12,
            )
            if k == "location":
                v = f"""{v["venue_name"]}\n{v["address"]}"""

            lbl_value = m3.Text(text=str(v), font_size=12)
            # Add key label
            self.grid_panel.add_component(lbl_key, row=row, col_xs=col, width_xs=3)
            # Add value label
            self.grid_panel.add_component(
                lbl_value, row=row, col_xs=col + 3, width_xs=3
            )
            # Move to next pair
            col += 6
            if col >= 12:
                col = 0
                row += 1
        self.cpanel_data.add_component(self.grid_panel, full_width_row=True)

        marker = GoogleMap.Marker(
            animation=GoogleMap.Animation.DROP,
            position=GoogleMap.LatLng(45.5152, -122.6784),
            title=m3.Text(
                text="The Morrison Residence\n456 Oak Avenue\nPortland, OR 97204"
            ),
            visible=True,
        )
        self.google_map_1.center = marker.position
        self.google_map_1.height = "150"
        self.google_map_1.zoom = 15
        self.google_map_1.add_component(marker)

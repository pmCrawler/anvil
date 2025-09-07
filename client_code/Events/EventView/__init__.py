from ._anvil_designer import EventViewTemplate
from anvil import *
import anvil.users
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import datetime
from collections import OrderedDict


class EventView(EventViewTemplate):
    def __init__(self, event_id=4270964888, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        lst_keys = [
            "event_datetime",
            "location",
            # "event_setting",
            "budget",
            "guest_count",
        ]

        self.cpanel_main.col_spacing = "none"
        self.cpanel_data.col_spacing = "none"
        self.grid_panel = GridPanel(spacing_above="None", spacing_below="None")

        event = anvil.server.call("get_event_by_id", event_id)
        key_vals = OrderedDict((k, event[k]) for k in lst_keys if k in event)
        cnt_tasks = anvil.server.call("get_event_task_count", event_id)

        self.heading_title.text = event["title"]
        self.txt_description.text = event["description"]

        row, col = 0, 0
        for k, v in key_vals.items():
            if k == "location":
                k = "Where"
                v = f"""{v["venue_name"]}\n{v["address"]}"""
            if k == "event_datetime":
                k = "When"
                v = datetime.strftime(
                    event["event_datetime"],
                    "%a, %b %d, %Y at %I:%M %p",
                )

            k = "Guests" if k == "guest_count" else k
            v = f"""${v}""" if k == "budget" else v

            lbl_key = m3.Text(text=k.title().replace("_", " "), bold=True, font_size=12)
            lbl_val = m3.Text(text=str(v), font_size=12)
            self.grid_panel.add_component(lbl_key, row=row, col_xs=col, width_xs=1)
            self.grid_panel.add_component(lbl_val, row=row, col_xs=col + 1, width_xs=4)
            # Move to next pair
            col += 6
            if col >= 12:
                col = 0
                row += 1
        self.cpanel_data.add_component(self.grid_panel)

        lbl_task_count = m3.Text(text="Tasks", bold=True, font_size=12)
        val_task_count = m3.Text(text=cnt_tasks, font_size=12)

        self.grid_panel.add_component(lbl_task_count, col_xs=0, width_xs=1)
        self.grid_panel.add_component(val_task_count, col_xs=1, width_xs=2)

        marker = GoogleMap.Marker(
            animation=GoogleMap.Animation.DROP,
            position=GoogleMap.LatLng(45.5152, -122.6784),
            title=m3.Text(
                text="The Morrison Residence\n456 Oak Avenue\nPortland, OR 97204"
            ),
            visible=True,
        )
        self.google_map_1.center = marker.position
        self.google_map_1.height = "100"
        self.google_map_1.zoom = 15
        self.google_map_1.add_component(marker)

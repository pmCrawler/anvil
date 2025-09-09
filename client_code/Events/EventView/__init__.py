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

        event_data, tasks, counts = anvil.server.call("get_event_data", event_id)
        self._bind_event_details(event_data)
        self._bind_task_details(tasks)

    def _bind_event_details(self, event_data):
        lst_keys = [
            "event_datetime",
            "location",
            "budget",
            "guest_count",
        ]

        self.heading_title.text = event_data["title"]
        self.txt_description.text = event_data["description"]

        key_vals = OrderedDict((k, event_data[k]) for k in lst_keys if k in event_data)
        row, col = 0, 0

        for k, v in key_vals.items():
            if k == "location":
                k = "Where"
                v = f"""{v["venue_name"]}\n{v["address"]}"""
            if k == "event_datetime":
                k = "When"
                v = datetime.strftime(
                    event_data["event_datetime"],
                    "%a, %b %-d, %Y @ %-I:%M %p",
                )

            k = "Guests" if k == "guest_count" else k
            v = f"""${v}""" if k == "budget" else v

            lbl_key = m3.Text(text=k.title().replace("_", " "), bold=True, font_size=12)
            lbl_val = m3.Text(text=str(v), font_size=12)
            self.gpnl_event.add_component(lbl_key, row=row, col_xs=col, width_xs=1)
            self.gpnl_event.add_component(lbl_val, row=row, col_xs=col + 1, width_xs=4)
            # Move to next pair
            col += 6
            if col >= 12:
                col = 0
                row += 1

        self._load_map_components(event_data["location"])

    def _bind_task_details(self, task_list):
        print(task_list)

        self.rpnl_tasks.items = task_list["tasks"]

        val_task_bg = None
        if task_list["pct_compl"] < 60:
            val_task_bg = "#f8a4af"  # red
        elif task_list["pct_compl"] >= 80:
            val_task_bg = "#97f9a4"  # green
        else:
            val_task_bg = "#f0b090"  # orange

        lbl_task_count = m3.Text(
            text="Tasks",
            bold=True,
            font_size=12,
        )
        val_task_count = m3.Text(
            text=f"""{task_list["compl_cnt"]} of {task_list["tot_cnt"]} done""",
            font_size=12,
            align="left",
            text_color=val_task_bg,
        )

        self.gpnl_event.add_component(lbl_task_count, col_xs=0, width_xs=1)
        self.gpnl_event.add_component(val_task_count, col_xs=1, width_xs=2)

    def _load_map_components(self, location):
        marker = GoogleMap.Marker(
            animation=GoogleMap.Animation.DROP,
            position=GoogleMap.LatLng(
                location["coordinates"]["lat"],
                location["coordinates"]["lng"],
            ),
            title=m3.Text(text=f"""{location["venue_name"]}\n{location["address"]}"""),
            visible=True,
        )
        self.google_map_1.center = marker.position
        self.google_map_1.height = "100"
        self.google_map_1.zoom = 15
        self.google_map_1.add_component(marker)

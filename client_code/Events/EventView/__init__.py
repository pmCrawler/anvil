from ._anvil_designer import EventViewTemplate
from anvil import *
import m3.components as m3
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import datetime
from collections import OrderedDict
from anvil_extras.persistence import persisted_class
from anvil_extras import popover
from ...Tasks.TaskForm import TaskForm


@persisted_class
class Event:
    key = "title"


class EventView(EventViewTemplate):
    def __init__(self, event_id=4270964888, **properties):
        self.init_components(**properties)

        self.event_id = event_id
        self.event_data, tasks, options = anvil.server.call("get_event_data", event_id)
        self._bind_event_details(self.event_data)
        self._bind_task_details(tasks)
        self._bind_budget_tracker(options["budget_tracker"])

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

            lbl_key = m3.Text(
                text=k.title().replace("_", " "),
                bold=True,
                font_size=12,
            )
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
        _tasks = sorted(task_list["tasks"], key=lambda t: t["due_date"])
        self.txt_count_done.text = f"""Done: {task_list["compl_cnt"]}"""
        self.txt_count_remains.text = f"""Remains: {task_list["incompl_cnt"]}"""
        self.rpnl_tasklist.items = _tasks

    def _bind_budget_tracker(self, bt):
        self.rpnl_budget.items = bt

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

    def btn_add_task_click(self, **event_args):
        task_form = TaskForm(event=self.event_data)
        task_form.set_event_handler("x-refresh_parent", self.refresh_tasks)

        self.btn_add_task.popover(
            task_form,
            placement="left",
            trigger="manual",
            auto_dismiss=True,
            max_width="500px",
        )
        self.btn_add_task.pop("show")

    def refresh_tasks(self, **event_args):
        task_list = anvil.server.call(
            "get_event_tasks",
            self.event_id,
        )
        self._bind_task_details(task_list)

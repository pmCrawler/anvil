from ._anvil_designer import TaskFormTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TaskForm(TaskFormTemplate):
    def __init__(self, event=None, source=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.source = source
        self.events = []
        if not event:
            self.events = anvil.server.call("get_events", user_id=None)
            self.dd_event_list.items = [ev["title"] for ev in self.events]
        else:
            self.events.append(event)
            self.dd_event_list.items = [ev["title"] for ev in self.events]
            self.dd_event_list.selected_value = event["title"]
        # self.refresh_comment_panel_items()

    # def refresh_comment_panel_items(self):
    #     self.comment_panel.items = anvil.server.call("get_comments", self.item)

    def btn_add_task_click(self, **event_args):
        """This method is called when the component is clicked."""

        selected_event = [
            ev for ev in self.events if ev["title"] == self.dd_event_list.selected_value
        ]
        app_tables.tasks.add_row(
            event_link=selected_event[0],
            task=self.txtbx_title.text,
            details=self.txtarea_details.text,
            due_date=self.dtpkr_due_date.date,
            duration=self.txtbx_duration.text,
            status=self.rgpnl_status.selected_value,
        )
        # Raise a custom event to notify the parent form
        self.raise_event("x-refresh_parent")

        # Inside TaskForm
        self.popper.pop("hide")

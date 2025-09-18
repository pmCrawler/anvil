from ._anvil_designer import TaskFormTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TaskForm(TaskFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.events = anvil.server.call("get_events", user_id=None)
        self.dd_event_list.items = [ev["title"] for ev in self.events]

    def btn_add_task_click(self, **event_args):
        """This method is called when the component is clicked."""

        ev_selected = [ev for ev in self.events if ev["title"] == self.dd_event_list.selected_value]
        event_link = ev_selected[0]
        task = app_tables.tasks.add_row(
            event_link=event_link,  # self.dd_event_list.selected_value,
            title=self.txtbx_title.text,
            details=self.txtarea_details.text,
            due_date=self.dtpkr_due_date.date,
            duration=self.txtbx_duration.text,
            status=self.rgpnl_status.selected_value,
        ).get_id()
        print(f"""Task Id: {task}""")

        open_form_from()
        # anvil.server.call("save_task", event_args)
        pass

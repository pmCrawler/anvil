from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime


class ItemTemplate2(ItemTemplate2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.txt_status.icon = "mi:check_box"
        if self.txt_status.text == "In progress":
            self.txt_status.text_color = self.txt_status.icon_color = "blue"
        elif self.txt_status.text == "Done":
            self.txt_status.text_color = self.txt_status.icon_color = "green"
        else:
            self.txt_status.text_color = self.txt_status.icon_color = "orange"

        fmt_time = self.txt_due_date.text
        self.txt_due_date.text = datetime.strftime(fmt_time, "%m-%d-%Y")

    def txt_task_show(self, **event_args):
        """This method is called when the component is shown on the screen."""
        pass

    def lnk_edit_task_click(self, **event_args):
        """This method is called clicked"""
        pass

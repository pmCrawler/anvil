from ._anvil_designer import EventFormTemplate
from anvil import *
import anvil.users
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Events
import anvil.http
import json


class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # self.event_ai.content_panel.visible = False
        self.event_ai.visible = False
        self.cpanel_options.visible = False
        self.user_input = dict()

        self._load_default_input()

    def _load_default_input(self):
        self.title.text = "Liverpool vs West Ham Football Match Viewing Party"
        self.description.text = "A gathering to watch the Liverpool vs West Ham football match with friends and family"
        self.datetime.date = "2025-11-30"
        self.guest_count.text = 10
        self.budget.text = 300
        self.venue_type.text = "home"

    def get_user_input(self):
        self.user_input = {
            "title": self.title.text,
            "description": self.description.text,
            "event_datetime": self.datetime.date,
            "guest_count": self.guest_count.text,
            "budget": self.budget.text,
            "venue_type": self.venue_type.text,
            "food_bev": True if self.switch_food.selected else False,
            "event_setting": self.rgp_setting.selected_value,
        }

    def btn_start_click(self, **event_args):
        """This method is called when the component is clicked."""

        details = anvil.server.call("get_user_events", 1)
        print(details)

        self.get_user_input()
        with anvil.server.no_loading_indicator:
            Notification("Running AI for your event...", timeout=5).show()

        try:
            result = anvil.server.call("create_event", **self.user_input)
        except Exception as e:
            print(f"Something went wrong: {e}")

        if result["success"]:
            self.btn_start.visible = False
            self.event_ai.visible = True
            self.event_ai.process_json_response(result["output"])
            self.cpanel_options.visible = True
        else:
            alert(f"Error: {result['error']}")

    def btn_save_click(self, **event_args):
        """This method is called when the component is clicked."""

        # FOR TESTING ONLY
        open_form("Events.EventView", event_id=4270964888)

        # # selections = self.event_ai.get_selected_values()
        # self.user_input.update({"ai_response": self.resp})
        # result = anvil.server.call("upsert_event_data", self.user_input)
        # if result["success"]:
        #     Notification(
        #         f"""Event and tasks saved! Task Count: {result["task_count"]}""",
        #         timeout=5,
        #     ).show()
        #     open_form("Events.EventView", event_id=result["event_id"])
        # else:
        #     Notification(f"Error: {result['error']}", timeout=5, style="danger").show()

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

from .. import ui_builder


# EventForm.py
class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.cpanel_options.visible = False
        self.user_input = dict()
        self.event_id = None  # Store event ID

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
        """Generate AI event plan"""

        self.btn_start.enabled = False
        self.get_user_input()

        with anvil.server.no_loading_indicator:
            Notification(
                "🤖 AI is creating your event plan...",
                timeout=3,
                style="info",
            ).show()

        self.btn_start.text = "⏳ Creating Plan..."

        try:
            # result = anvil.server.call("create_event", **self.user_input)
            result = anvil.server.call("get_event_with_ai_plan", 24)

            if result["success"]:
                # Store event ID
                self.event_id = result["event"]["id"]

                # Add event_id to output for save function
                ai_plan_data = result["ai_plan"]
                ai_plan_data["event_id"] = self.event_id

                # Hide form, show AI results
                self.btn_start.visible = False

                ui_builder.build_event_plan_ui(ai_plan_data, self.cpanel_options)
                self.cpanel_options.visible = True

                # Success notification
                Notification(
                    f"✅ Event plan created! Event ID: {self.event_id}",
                    timeout=3,
                    style="success",
                ).show()
            else:
                alert(f"Error:\n{result['error']}", title="Error")
                self.btn_start.enabled = True
                self.btn_start.text = "🎉 Start Planning"

        except Exception as e:
            print(f"Exception: {e}")
            import traceback

            traceback.print_exc()

            alert(f"An error occurred:\n{str(e)}", title="Error")
            self.btn_start.enabled = True
            self.btn_start.text = "🎉 Start Planning"

    # def btn_save_click(self, **event_args):
    #     """This method is called when the component is clicked."""

    #     # FOR TESTING ONLY
    #     open_form("Events.EventView", event_id=4270964888)

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

# import asyncio


QUESTION_WF_URL = "http://localhost:5678/webhook/69aee61f-e514-417d-ad16-0615b6e1a9c9"
EVENT_WF_URL = "http://localhost:5678/webhook/dafb4274-ddf0-4874-a0e1-5a362c525170"


class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # self.event_ai.content_panel.visible = False
        self.event_ai.visible = False
        self.cpanel_options.visible = False
        self.user_input = dict()

        self._load_default_input()

    def button_search_address_click(self, **event_args):
        """Search for address using server-side geocoding"""
        address_query = self.text_box_address.text

        if not address_query:
            alert("Please enter an address")
            return

        # Show loading
        with anvil.server.no_loading_indicator:
            Notification("Searching for address...", timeout=2).show()

        # Call server
        results = anvil.server.call("geocode_address", address_query)

        if results["success"]:
            # Show results in dropdown
            self.show_address_results(results["addresses"])
        else:
            alert(f"Error: {results['error']}")

    def show_address_results(self, addresses):
        """Display address options to user"""
        # Show results in repeating panel or dropdown
        self.dropdown_address_results.items = [
            addr["formatted_address"] for addr in addresses
        ]
        self.dropdown_address_results.visible = True

    def dropdown_address_results_change(self, **event_args):
        """User selected an address"""
        selected = self.dropdown_address_results.selected_value

        if selected:
            self.location_data = selected
            self.label_selected_address.text = selected["formatted_address"]
            self.button_save.enabled = True

    def address_selected(self, address_data):
        """Called when user selects address from autocomplete"""
        print(f"Address selected: {address_data}")

        # Store address data
        self.location_data = {
            "formatted_address": address_data["formatted_address"],
            "latitude": address_data["latitude"],
            "longitude": address_data["longitude"],
            "city": address_data["components"].get("city"),
            "region": address_data["components"].get("region"),
            "region_code": address_data["components"].get("region_code"),
            "postal_code": address_data["components"].get("postal_code"),
            "country": address_data["components"].get("country"),
            "country_code": address_data["components"].get("country_code"),
        }

        # Display formatted address
        self.text_box_address.text = address_data["formatted_address"]

        # Optionally show details
        self.label_city.text = f"City: {self.location_data.get('city', 'N/A')}"
        self.label_country.text = f"Country: {self.location_data.get('country', 'N/A')}"

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
            "event_date": self.datetime.date,
            "guest_count": self.guest_count.text,
            "total_budget": self.budget.text,
            "venue_type": self.venue_type.text,
            "food_bev": True if self.switch_food.selected else False,
            "event_setting": self.rgp_setting.selected_value,
        }
        # return self.user_input

    def btn_start_click(self, **event_args):
        """This method is called when the component is clicked."""

        self.btn_start.visible = False
        self.get_user_input()
        self.resp = anvil.server.call("run_event_ai", self.user_input)
        self.event_ai.visible = True
        self.event_ai.process_json_response(self.resp)
        self.cpanel_options.visible = True

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

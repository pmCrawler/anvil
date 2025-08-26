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

QUESTION_WF_URL = "http://localhost:5678/webhook/69aee61f-e514-417d-ad16-0615b6e1a9c9"
EVENT_WF_URL = "http://localhost:5678/webhook/dafb4274-ddf0-4874-a0e1-5a362c525170"


class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        # self.event_ai.content_panel.visible = False
        self.user_input = dict()
        self.event_ai.visible = False
        self.btn_save.visible = False

    def btn_start_click(self, **event_args):
        """This method is called when the component is clicked."""

        self.user_input = self.get_user_input()
        # resp = anvil.http.request(EVENT_WF_URL, data=self.user_input, json=True)
        self.resp = self.event_ai.load_sample_data()

        self.btn_start.visible = False
        self.event_ai.visible = True
        self.event_ai.process_json_response(self.resp)
        self.btn_save.visible = True

    def get_user_input(self):
        self.user_input = {
            "title": self.input_title.text,
            "description": self.input_description.text,
            "event_datetime": self.input_datetime.date,
            "guest_count": self.input_guest_count.text,
            "budget": self.input_budget.text,
            "venue_type": self.input_venue_type.text,
            "food_bev": True if self.switch_food.selected else False,
            "event_setting": self.rgp_setting.selected_value,
        }
        return self.user_input

    def btn_save_click(self, **event_args):
        """This method is called when the component is clicked."""

        self.user_input.update({"ai_response": self.resp})
        id = anvil.server.call("save_event", self.user_input)
        print(id)
        pass

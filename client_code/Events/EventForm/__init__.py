from ._anvil_designer import EventFormTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Events
import anvil.http
from pprint import pprint



QUESTION_WF_URL = "http://localhost:5678/webhook/69aee61f-e514-417d-ad16-0615b6e1a9c9"
EVENT_WF_URL = "http://localhost:5678/webhook/dafb4274-ddf0-4874-a0e1-5a362c525170"


class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.cpanel_questions.visible = False
        self.cpanel_summary.visible = False

        self.description = ""
        self.current_question = ""

        self.answers = []
        self.user_input = {}

    def btn_start_click(self, **event_args):
        """This method is called when the component is clicked."""

        self.btn_start.visible = False
        self.cpanel_questions.visible = True
        self.cpanel_start.visible = True
        self.start_wizard()

    def start_wizard(self):
        """Start Q&A wizard to collect more info using dynamic AI-driven questions."""

        self.user_input = self.get_user_input()
        resp = anvil.http.request(QUESTION_WF_URL, data=self.user_input, json=True)

        pprint(resp)
        self.current_question = resp
        self.label_question.text = self.current_question

    def btn_submit_answer_click(self, **event_args):
        """This method is called when the component is clicked."""

        answer = self.input_answer.text
        self.answers.append({"question": self.current_question, "answer": answer})
        self.user_input.update({"qna": self.answers})

        self.input_answer.text = ""
        resp = anvil.http.request(QUESTION_WF_URL, data=self.user_input, json=True)

        if not resp or resp["question"] == "Thanks! That's all I need to get started.":
            self.label_question.text = resp["question"]
            self.input_answer.visible = False
            self.btn_submit_answer.visible = False

            self.cpanel_summary.visible = True
            self.rpanel_qna.items = self.answers
        else:
            next_q = anvil.http.request(
                QUESTION_WF_URL, data=self.user_input, json=True
            )
            self.current_question = next_q
            self.label_question.text = self.current_question

    def btn_call_ai_click(self, **event_args):
        """This method is called when the component is clicked."""

        pprint(self.user_input)
        resp = anvil.http.request(EVENT_WF_URL, data=self.user_input, json=True)
        pass
        open_form("Events.EventAI", **resp)

    def get_user_input(self):
        self.user_input = {
            "event_title": self.input_title.text,
            "event_description": self.input_description.text,
            "event_datetime": str(self.input_datetime.date),
            "guest_count": self.input_guest_count.text,
            "budget": self.input_budget.text,
            "venue_type": self.input_venue_type.text,
            "food_bev": True if self.switch_food.selected else False,
            "event_setting": self.rgp_setting.selected_value,
            "qna": self.answers,
        }
        return self.user_input

from ._anvil_designer import EventFormTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ... import Events


class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.description = ""
        self.current_question = ""
        self.answers = []
        self.count = 0
        self.cpanel_questions.visible = False
        self.cpanel_summary.visible = False

    def btn_submit_answer_click(self, **event_args):
        """This method is called when the component is clicked."""

        self.count += 1
        answer = self.input_answer.text
        self.answers.append({"question": self.current_question, "answer": answer})
        self.input_answer.text = ""

        if self.count == 2:
            self.label_question.text = (
                "Thanks! You're all set. Submit to get the party started!"
            )
            self.input_answer.visible = False
            self.btn_submit_answer.visible = False

            self.cpanel_summary.visible = True
            self.rpanel_qna.items = self.answers
        else:
            next_q = anvil.server.call(
                "generate_next_question",
                self.description,
                self.answers,
            )
            self.current_question = f"""{next_q}_{self.count}"""
            self.label_question.text = self.current_question

    def btn_start_click(self, **event_args):
        """This method is called when the component is clicked."""
        self.start_wizard()
        self.btn_start.visible = False
        self.cpanel_questions.visible = True
        self.cpanel_start.visible = True

    def start_wizard(self):
        self.description = self.input_description.text
        self.current_question = anvil.server.call(
            "generate_next_question",
            self.description,
            [],
        )
        self.label_question.text = self.current_question

    def btn_call_ai_click(self, **event_args):
        """This method is called when the component is clicked."""

        user_input = {
            "event_title": self.input_title,
            "event_description": self.input_description.text,
            "event_datetime": self.input_datetime,
            "guest_count": self.input_guest_count,
            "budget": self.input_budget,
            "venue_type": self.input_venue,
            "food_bev": True if self.switch_food.selected else False,
            "event_setting": self.rgp_setting.selected_value,
        }
        resp = anvil.server.call("get_ai_response", user_input)
        open_form("Events.EventAI", **resp)
        pass

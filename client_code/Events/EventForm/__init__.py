from ._anvil_designer import EventFormTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class EventForm(EventFormTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.description = ""
        self.answers = []
        self.current_question = ""

    def btn_submit_answer_click(self, **event_args):
        """This method is called when the component is clicked."""
        answer = self.txt_answer_input.text
        self.answers.append((self.current_question, answer))
        self.txt_answer_input.text = ""

        next_q = anvil.server.call(
            "generate_next_question",
            self.description,
            self.answers,
        )

        if "That's all I need" in next_q:
            self.txt_question_label.text = "Thanks! You're all set."
            self.submit_answer_btn.enabled = False
        else:
            self.current_question = next_q
            self.txt_question_label.text = next_q

    def start_wizard(self):
        self.description = self.txt_input_description.text
        self.answers = []
        self.current_question = anvil.server.call(
            "generate_next_question", self.description, []
        )
        self.txt_question_label.text = self.current_question

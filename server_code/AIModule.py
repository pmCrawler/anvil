import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http

# import openai  # or your preferred AI provider

# openai.api_key = "your-openai-api-key"
inputs = {
    "event_title": "sample event",
    "event_description": "hosting my first book club event",
    "event_type": "book club",
    "event_date": "4/4/2026",
    "guest_count": 30,
    "venue_type": "club house",
    "food_bev": True,
    "event_setting": "indoor",
}
n8n_url = "http://localhost:5678/webhook/dafb4274-ddf0-4874-a0e1-5a362c525170"


@anvil.server.callable
def get_ai_response(user_input):
    # return "call to get_event_data"
    ai_resp = {}
    resp = anvil.http.request(n8n_url, data=user_input, json=True)
    ai_resp = resp["data"][0]["message"]["content"]
    return ai_resp


@anvil.server.callable
def generate_next_question(description, answers):
    history = "\n".join([
        f"Q{i + 1}: {q}\nA{i + 1}: {a}" for i, (q, a) in enumerate(answers)
    ])

    prompt = f"""You are an intelligent assistant helping a user plan an event. Initial description: "{description}" Conversation so far: {history}
                Ask the next most relevant question to clarify their needs. If everything is clear, say "That's all I need for now." """

    # response = openai.ChatCompletion.create(
    #     model="gpt-4o",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.7,
    # )

    # next_question = response["choices"][0]["message"]["content"].strip()
    return "What's your name?"  # next_question

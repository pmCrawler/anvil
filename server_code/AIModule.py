import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
# import openai  # or your preferred AI provider

# openai.api_key = "your-openai-api-key"


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

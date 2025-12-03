import anvil.users
import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

from .models import EventDetails, EventPlan
import asyncio
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from .prompts import system_prompt, user_prompt


openai_api_key = anvil.secrets.get_secret("openai_api_key")
model = OpenAIChatModel(
    "gpt-4o-mini",
    provider=OpenAIProvider(api_key=openai_api_key),
)

# Create the agent
event_agent = Agent(
    model=model,
    deps_type=EventDetails,
    output_type=EventPlan,
    system_prompt=system_prompt,
)


@event_agent.system_prompt
async def add_dynamic_instructions(ctx: RunContext[EventDetails]) -> str:
    """Add event-specific context to the system prompt"""

    budget_per_person = ctx.deps.total_budget / ctx.deps.guest_count

    return f"""
    Current Event Details:
    - Title: {ctx.deps.title}
    - Description: {ctx.deps.description}
    - Date: {ctx.deps.event_date}
    - Guest Count: {ctx.deps.guest_count}
    - Total Budget: ${ctx.deps.total_budget} (${budget_per_person:.2f} per person)
    - Venue: {ctx.deps.venue_type}
    
    Important: Create a complete response with ALL required fields filled out.
    Scale all suggestions appropriately for {ctx.deps.guest_count} guests and ${ctx.deps.total_budget} budget.
    """


@anvil.server.callable
def run_ai(user_input):
    event = EventDetails(
        title=user_input["title"],
        description=user_input["description"],
        event_date=user_input["event_datetime"],
        guest_count=int(user_input["guest_count"]),
        total_budget=int(user_input["budget"]),
        venue_type=user_input["venue_type"],
    )

    try:
        result = await event_agent.run(
            user_prompt=user_prompt,
            deps=event,
        )
        # Save to file
        output = result.output.model_dump()
        output["input_event_details"] = event.__dict__
        return output
    except Exception as e:
        print(f"✗ Error planning {event.title}: {str(e)}")


@anvil.server.callable
def get_event_details():
    event = EventDetails(
        title="Liverpool vs West Ham Football Match Viewing Party",
        description="A gathering to watch the Liverpool vs West Ham football match with friends and family",
        event_date="2025-11-30",
        guest_count=10,
        total_budget=300,
        venue_type="home",
    )
    return event.__dict__()

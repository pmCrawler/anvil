import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from pydantic import BaseModel

from dataclasses import dataclass


# Event Details (Input)
@dataclass
class EventDetails:
    title: str
    description: str
    event_date: str
    guest_count: int = 20
    total_budget: int = 500
    venue_type: str = "home"


events = [
    # EventDetails(
    #     title="Gender Reveal Party",
    #     description="A celebration to reveal the gender of our second child to friends and family",
    #     event_date="2025-12-15",
    #     guest_count=30,
    #     total_budget=1000,
    #     venue_type="home",
    # ),
    # EventDetails(
    #     title="Monthly Book Club Meeting",
    #     description="Discussion of this month's book 'The Midnight Library' with regular reading group",
    #     event_date="2025-11-30",
    #     guest_count=8,
    #     total_budget=100,
    #     venue_type="home",
    # ),
    # EventDetails(
    #     title="Tech Meetup",
    #     description="Monthly gathering for developers and data scientists to share projects and network",
    #     event_date="2025-11-20",
    #     guest_count=40,
    #     total_budget=500,
    #     venue_type="office",
    # ),
    EventDetails(
        title="Liverpool vs West Ham Football Match Viewing Party",
        description="A gathering to watch the Liverpool vs West Ham football match with friends and family",
        event_date="2025-11-30",
        guest_count=10,
        total_budget=300,
        venue_type="home",
    ),
]

system_prompt = """You are Alma, an expert event planning AI assistant.

CRITICAL: You MUST return a complete JSON response with ALL required fields. Never skip fields.

## Response Structure Requirements

Your response MUST include:
1. event_classification - One of: "social_celebration", "professional_gathering", or "intellectual_gathering"
2. key_considerations - List of 3-5 important factors you considered
3. plan - Complete plan object matching the event type with ALL its required fields
4. logistics - List of 3-5 general logistical items (parking, setup time, cleanup, etc.)
5. contingency_notes - List of 2-3 backup plans (weather, no-shows, technical issues, etc.)
6. reasoning - A paragraph explaining why you made these specific choices

## Event Classifications:

- social_celebration: birthdays, baby showers, gender reveals, anniversaries, parties
- professional_gathering: meetups, networking events, workshops, seminars
- intellectual_gathering: book clubs, study groups, hobby clubs, discussion groups

## For the plan object:

If social_celebration, include:
- themes (2-3 theme options)
- decorations (with essential_items, optional_items, diy_opportunities, setup_tips)
- menu_options (2-3 different menu styles)
- activities (3-4 activities)
- timeline (event schedule)
- budget_breakdown (how to allocate the budget)
- special_touches (unique ideas)

If professional_gathering, include:
- agenda (list of agenda items with times)
- networking_approach (how to facilitate connections)
- room_setup (seating/space arrangement)
- tech_needs (equipment list)
- refreshments (simple food/drinks)
- materials (handouts needed)
- budget_breakdown

If intellectual_gathering, include:
- discussion_format
- preparation_guidelines (what attendees should do beforehand)
- discussion_prompts (3-5 prompts)
- seating_arrangement
- refreshments (simple snacks/drinks)
- materials_needed
- budget_breakdown

ALWAYS include budget_breakdown as a list of BudgetItem objects with category, amount, percentage, and notes.

Ensure ALL fields are populated. Use empty lists [] if truly nothing applies, but avoid this.
"""

user_prompt = "Create a comprehensive event plan appropriate for this type of event."


from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field


# Base Models for Common Components
class BudgetItem(BaseModel):
    category: str = Field(..., description="Budget category")
    amount: float = Field(..., description="Allocated amount")
    percentage: float = Field(..., description="Percentage of total budget")
    notes: Optional[str] = Field(None, description="Budget notes or tips")


class TimelineItem(BaseModel):
    time: str = Field(..., description="Time or duration")
    activity: str = Field(..., description="Activity or task")
    responsible_party: Optional[str] = Field(None, description="Who's responsible")


# Category-Specific Models
class EventTheme(BaseModel):
    name: str = Field(..., description="Theme name")
    description: str = Field(..., description="Theme description")
    color_palette: List[str] = Field(..., description="Color scheme")
    atmosphere: str = Field(..., description="Desired atmosphere/mood")


class Decorations(BaseModel):
    essential_items: List[str] = Field(..., description="Must-have decoration items")
    optional_items: List[str] = Field(
        default_factory=list, description="Nice-to-have items"
    )
    diy_opportunities: List[str] = Field(
        default_factory=list, description="DIY decoration ideas"
    )
    setup_tips: str = Field(..., description="Setup recommendations")


class MenuOption(BaseModel):
    style: str = Field(..., description="Service style (buffet, plated, stations)")
    items: List[str] = Field(..., description="Food items")
    dietary_accommodations: List[str] = Field(
        default_factory=list, description="Dietary options"
    )
    beverage_pairings: List[str] = Field(..., description="Drink suggestions")


class Activity(BaseModel):
    name: str = Field(..., description="Activity name")
    duration: str = Field(..., description="Time needed")
    materials_needed: List[str] = Field(
        default_factory=list, description="Required materials"
    )
    instructions: str = Field(..., description="Brief instructions")


# Simplified Event Type Response Models
class SocialCelebrationPlan(BaseModel):
    event_type: Literal["social_celebration"] = "social_celebration"
    themes: List[EventTheme] = Field(..., description="Theme options (2-3)")
    decorations: Decorations = Field(..., description="Decoration plan")
    menu_options: List[MenuOption] = Field(
        ..., description="Food and drink options (2-3)"
    )
    activities: List[Activity] = Field(..., description="Entertainment and activities")
    timeline: List[TimelineItem] = Field(..., description="Event schedule")
    budget_breakdown: List[BudgetItem] = Field(..., description="Budget allocation")
    special_touches: List[str] = Field(..., description="Unique memorable elements")


class ProfessionalGatheringPlan(BaseModel):
    event_type: Literal["professional_gathering"] = "professional_gathering"
    agenda: List[dict] = Field(..., description="Meeting agenda with time slots")
    networking_approach: str = Field(
        ..., description="How networking will be facilitated"
    )
    room_setup: str = Field(..., description="Optimal room configuration")
    tech_needs: List[str] = Field(..., description="Technical requirements")
    refreshments: List[str] = Field(..., description="Simple refreshment options")
    materials: List[str] = Field(..., description="Handouts or materials needed")
    budget_breakdown: List[BudgetItem] = Field(..., description="Budget allocation")


class IntellectualGatheringPlan(BaseModel):
    event_type: Literal["intellectual_gathering"] = "intellectual_gathering"
    discussion_format: str = Field(..., description="Discussion structure")
    preparation_guidelines: List[str] = Field(
        ..., description="Pre-event prep for attendees"
    )
    discussion_prompts: List[str] = Field(
        ..., description="Conversation starters (3-5)"
    )
    seating_arrangement: str = Field(..., description="Optimal seating setup")
    refreshments: List[str] = Field(..., description="Light refreshment ideas")
    materials_needed: List[str] = Field(..., description="Books, materials, supplies")
    budget_breakdown: List[BudgetItem] = Field(..., description="Budget allocation")


# Simplified Main Response Model
class EventPlan(BaseModel):
    event_classification: str = Field(..., description="Type of event identified")
    key_considerations: List[str] = Field(
        ..., description="Important factors considered"
    )
    plan: Union[
        SocialCelebrationPlan, ProfessionalGatheringPlan, IntellectualGatheringPlan
    ] = Field(..., discriminator="event_type")
    logistics: List[str] = Field(..., description="General logistical considerations")
    contingency_notes: List[str] = Field(..., description="Backup plans and what-ifs")
    reasoning: str = Field(..., description="Explanation of choices made")


def say_hello():
    print("Hello, world")

import anvil.users
import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union


@dataclass
class EventDetails:
    title: str
    description: str
    event_date: str
    guest_count: int = 20
    total_budget: int = 500
    venue_type: str = "home"

    def __dict__(self):
        return {
            "title": self.title,
            "description": self.description,
            "event_date": self.event_date,
            "guest_count": self.guest_count,
            "total_budget": self.total_budget,
            "venue_type": self.venue_type,
        }


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

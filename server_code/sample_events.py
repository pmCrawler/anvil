from .models import EventDetails

events = [
    EventDetails(
        title="Gender Reveal Party",
        description="A celebration to reveal the gender of our second child to friends and family",
        event_date="2025-12-15",
        guest_count=30,
        total_budget=1000,
        venue_type="home",
    ),
    EventDetails(
        title="Monthly Book Club Meeting",
        description="Discussion of this month's book 'The Midnight Library' with regular reading group",
        event_date="2025-11-30",
        guest_count=8,
        total_budget=100,
        venue_type="home",
    ),
    EventDetails(
        title="Tech Meetup",
        description="Monthly gathering for developers and data scientists to share projects and network",
        event_date="2025-11-20",
        guest_count=40,
        total_budget=500,
        venue_type="office",
    ),
]

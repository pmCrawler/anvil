import anvil.users
import anvil.secrets
import anvil.files
import anvil.server
import anvil.tables
from anvil.tables import app_tables


@anvil.server.callable
def get_event(id):
    event = (e for e in EVENTS if e["id"] == id)
    return event


@anvil.server.callable
def get_events(user_id):
    return EVENTS


@anvil.server.callable
@anvil.tables.in_transaction
def save_event(user_input):
    event = app_tables.event.add_row(
        title=user_input["title"],
        description=user_input["description"],
        event_datetimetime=user_input["event_datetimetime"],
        venue_type=user_input["venue_type"],
        guest_count=user_input["guest_count"],
        budget=user_input["budget"],
        food_bev=user_input["food_bev"],
        event_setting=user_input["event_setting"],
        ai_response=user_input["ai_response"],
        location={
            "venue_name": "The Morrison Residence",
            "address": "456 Oak Avenue, Portland, OR 97204",
            "coordinates": {"lat": 45.5152, "lng": -122.6784},
            "indoor": True,
        },
    )

    tasks = user_input["tasks"]
    app_tables.tasks.add_row(event_id=event.get_id())
    return event


EVENTS = [
    {
        "title": "Mystery Book Club: And Then There Were None",
        "description": "Join us for a thrilling discussion of Agatha Christie's masterpiece 'And Then There Were None'. We'll explore the intricate plot twists and Christie's genius in crafting the perfect murder mystery.",
        "event_type": "book club",
        "event_is_public": True,
        "location": {
            "venue_name": "Riverside Community Library",
            "address": "123 Main Street, Seattle, WA 98101",
            "coordinates": {"lat": 47.6062, "lng": -122.3321},
            "indoor": True,
        },
        "event_status": "published",
        "event_datetime": "2025-02-15",
        "event_start": "14:00",
        "event_end": "16:00",
        "budget": 150,
        "guest_count": 15,
    },
    {
        "title": "Sarah's Baby Shower - Ocean Theme",
        "description": "Celebrate the upcoming arrival of baby Emma with an ocean-themed baby shower. Games, gifts, and seafood appetizers await!",
        "event_type": "baby shower",
        "event_is_public": False,
        "location": {
            "venue_name": "The Morrison Residence",
            "address": "456 Oak Avenue, Portland, OR 97204",
            "coordinates": {"lat": 45.5152, "lng": -122.6784},
            "indoor": True,
        },
        "event_status": "published",
        "event_datetime": "2025-03-08",
        "event_start": "11:00",
        "event_end": "14:30",
        "budget": 800,
        "guest_count": 25,
    },
    {
        "title": "Spring Gardening Workshop",
        "description": "Learn the basics of spring planting, soil preparation, and organic gardening techniques. Perfect for beginners and experienced gardeners alike.",
        "event_type": "gardening club",
        "event_is_public": True,
        "location": {
            "venue_name": "Green Thumb Gardens",
            "address": "789 Garden Way, Austin, TX 78701",
            "coordinates": {"lat": 30.2672, "lng": -97.7431},
            "indoor": False,
        },
        "event_status": "published",
        "event_datetime": "2025-03-22",
        "event_start": "10:00",
        "event_end": "12:30",
        "budget": 300,
        "guest_count": 20,
    },
    {
        "title": "Emily's 30th Birthday Bash",
        "description": "Join us for a Great Gatsby themed birthday celebration! Dress in your best 1920s attire for an evening of jazz, cocktails, and dancing.",
        "event_type": "birthday",
        "event_is_public": False,
        "location": {
            "venue_name": "The Roosevelt Ballroom",
            "address": "321 Broadway, New York, NY 10007",
            "coordinates": {"lat": 40.7128, "lng": -74.0060},
            "indoor": True,
        },
        "event_status": "published",
        "event_datetime": "2025-04-12",
        "event_start": "19:00",
        "event_end": "22:00",
        "budget": 2500,
        "guest_count": 30,
    },
    {
        "title": "Wine & Paint Night",
        "description": "Unleash your creativity while sipping on fine wines. Professional artist guidance provided. All materials included.",
        "event_type": "social",
        "event_is_public": True,
        "location": {
            "venue_name": "Artisan Studio",
            "address": "654 Artist Lane, San Francisco, CA 94102",
            "coordinates": {"lat": 37.7749, "lng": -122.4194},
            "indoor": True,
        },
        "event_status": "published",
        "event_datetime": "2025-02-28",
        "event_start": "18:00",
        "event_end": "20:30",
        "budget": 600,
        "guest_count": 18,
    },
]

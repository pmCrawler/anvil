# ============================================================================
# CONFIGURATION - Define rendering rules for different content types

# How to Add New Sections
# Example: Add "Venue Suggestions" section

# # Just add to SECTION_CONFIG:
# SECTION_CONFIG['venue_suggestions'] = {
#     'title': '🏛️ Venue Suggestions',
#     'color': '#1976d2',
#     'icon': 'mi:location_city',
#     'initially_open': True,
#     'renderer': 'card_list',
#     'card_type': 'venue'
# }

# # Add card type config:
# CARD_TYPES['venue'] = {
#     'title_key': 'name',
#     'fields': [
#         {'key': 'address', 'type': 'text'},
#         {'key': 'capacity', 'type': 'inline', 'prefix': '👥'},
#         {'key': 'amenities', 'type': 'bullet_list', 'label': 'Amenities:'},
#         {'key': 'price_range', 'type': 'key_value'}
#     ]
# }

# # That's it! No code changes needed.

# ============================================================================

# Section configurations: defines how each section should be rendered
# ============================================================================
# CONFIGURATION with RANKING
# ============================================================================

SECTION_CONFIG = {
    # Special sections (rendered separately)
    "event_classification": {
        "rank": 0,  # Header - rendered first
        "renderer": "header",
        "skip_in_plan": True,
    },
    "key_considerations": {
        "rank": 1,
        "title": "🎯 Key Considerations",
        "color": "#2e7d32",
        "renderer": "key_considerations",
        "skip_in_plan": True,  # Handled separately
    },
    # Social Celebration sections
    "themes": {
        "rank": 2,
        "title": "🎨 Theme Options",
        "color": "#673ab7",
        "icon": "mi:palette",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "theme",
        "selectable": True,
        "selection_label": "Theme",
    },
    "decorations": {
        "rank": 3,
        "title": "🎈 Decorations",
        "color": "#e91e63",
        "icon": "mi:celebration",
        "initially_open": False,
        "renderer": "structured_list",
        "subsections": {
            "essential_items": {"label": "🔴 Essential Items:", "color": "#d32f2f"},
            "optional_items": {"label": "🔵 Optional Items:", "color": "#1976d2"},
            "diy_opportunities": {"label": "✂️ DIY Opportunities:", "color": "#388e3c"},
            "setup_tips": {"label": "💡 Setup Tips:", "style": "info_card"},
        },
        "selectable": False,
    },
    "menu_options": {
        "rank": 4,
        "title": "🍽️ Menu Options",
        "color": "#ff6f00",
        "icon": "mi:restaurant",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "menu",
        "selectable": True,
        "selection_label": "Menu",
    },
    "activities": {
        "rank": 5,
        "title": "🎮 Activities",
        "color": "#9c27b0",
        "icon": "mi:sports_esports",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "activity",
        "selectable": True,
        "selection_label": "Activity",
        "multi_select": True,
    },
    "timeline": {
        "rank": 7,
        "title": "⏰ Event Timeline",
        "color": "#1976d2",
        "icon": "mi:schedule",
        "initially_open": False,
        "renderer": "timeline",
        "selectable": False,
        "save_to_table": True,
    },
    "budget_breakdown": {
        "rank": 6,
        "title": "💰 Budget Breakdown",
        "color": "#4caf50",
        "icon": "mi:account_balance_wallet",
        "initially_open": False,
        "renderer": "budget",
        "selectable": False,
        "save_to_table": True,
    },
    "special_touches": {
        "rank": 8,
        "title": "✨ Special Touches",
        "color": "#ffd700",
        "icon": "mi:star",
        "initially_open": False,
        "renderer": "simple_list",
        "selectable": True,
        "selection_label": "Special Touch",
        "multi_select": True,
    },
    # Professional Gathering sections
    "agenda": {
        "rank": 3,
        "title": "📋 Agenda",
        "color": "#1976d2",
        "icon": "mi:list_alt",
        "initially_open": True,
        "renderer": "card_list",
        "card_type": "generic",
    },
    "networking_approach": {
        "rank": 4,
        "title": "🤝 Networking",
        "color": "#388e3c",
        "icon": "mi:groups",
        "initially_open": False,
        "renderer": "text",
    },
    "room_setup": {
        "rank": 5,
        "title": "🏢 Room Setup",
        "color": "#ff9800",
        "icon": "mi:meeting_room",
        "initially_open": False,
        "renderer": "text",
    },
    "tech_needs": {
        "rank": 6,
        "title": "💻 Tech Requirements",
        "color": "#f44336",
        "icon": "mi:computer",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "refreshments": {
        "rank": 7,
        "title": "☕ Refreshments",
        "color": "#795548",
        "icon": "mi:local_cafe",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "materials": {
        "rank": 8,
        "title": "📄 Materials",
        "color": "#607d8b",
        "icon": "mi:description",
        "initially_open": False,
        "renderer": "simple_list",
    },
    # Intellectual Gathering sections
    "discussion_format": {
        "rank": 3,
        "title": "💬 Discussion Format",
        "color": "#7b1fa2",
        "icon": "mi:forum",
        "initially_open": True,
        "renderer": "text",
    },
    "preparation_guidelines": {
        "rank": 4,
        "title": "📚 Preparation",
        "color": "#5e35b1",
        "icon": "mi:school",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "discussion_prompts": {
        "rank": 5,
        "title": "💡 Discussion Prompts",
        "color": "#7b1fa2",
        "icon": "mi:lightbulb",
        "initially_open": True,
        "renderer": "numbered_list",
    },
    "seating_arrangement": {
        "rank": 6,
        "title": "🪑 Seating",
        "color": "#388e3c",
        "icon": "mi:event_seat",
        "initially_open": False,
        "renderer": "text",
    },
    "materials_needed": {
        "rank": 7,
        "title": "📖 Materials",
        "color": "#e64a19",
        "icon": "mi:book",
        "initially_open": False,
        "renderer": "simple_list",
    },
    # Common sections (appear at end)
    "logistics": {
        "rank": 98,
        "title": "Logistics",
        "color": "#3f51b5",
        "icon": "mi:local_shipping",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "contingency_notes": {
        "rank": 99,
        "title": "Contingency Plans",
        "color": "#f44336",
        "icon": "mi:security",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "reasoning": {
        "rank": 100,  # Last
        "title": "💭 AI Reasoning",
        "color": "#9c27b0",
        "icon": "mi:psychology",
        "initially_open": False,
        "renderer": "text",
    },
}

# Card type configurations (unchanged)
CARD_TYPES = {
    "theme": {
        "title_key": "name",
        "fields": [
            {"key": "description", "type": "text"},
            {"key": "color_palette", "type": "color_palette"},
            {"key": "atmosphere", "type": "key_value"},
        ],
    },
    "menu": {
        "title_key": "style",
        "fields": [
            {"key": "items", "type": "bullet_list", "label": "Menu Items:"},
            {
                "key": "dietary_accommodations",
                "type": "bullet_list",
                "label": "🌱 Dietary:",
                "skip_if_empty": True,
            },
            {
                "key": "beverage_pairings",
                "type": "bullet_list",
                "label": "🥤 Beverages:",
            },
        ],
    },
    "activity": {
        "title_key": "name",
        "fields": [
            {"key": "duration", "type": "inline", "prefix": "⏱️"},
            {"key": "instructions", "type": "text", "italic": True},
            {
                "key": "materials_needed",
                "type": "bullet_list",
                "label": "📦 Materials:",
                "skip_if_empty": True,
            },
        ],
    },
    "generic": {"fields": [{"key": "*", "type": "auto"}]},
}

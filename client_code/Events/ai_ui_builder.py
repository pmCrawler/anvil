# ClientModules/ai_ui_builder.py

"""
Generic Dynamic UI Builder for AI Responses
Configuration-driven, reusable, and loosely coupled
"""

from anvil import *
import anvil.server
import m3.components as m3

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
SECTION_CONFIG = {
    # Social Celebration sections
    "themes": {
        "title": "🎨 Theme Options",
        "color": "#673ab7",
        "icon": "mi:palette",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "theme",
    },
    "decorations": {
        "title": "🎈 Decorations",
        "color": "#e91e63",
        "icon": "mi:celebration",
        "initially_open": True,
        "renderer": "structured_list",
        "subsections": {
            "essential_items": {"label": "🔴 Essential Items:", "color": "#d32f2f"},
            "optional_items": {"label": "🔵 Optional Items:", "color": "#1976d2"},
            "diy_opportunities": {"label": "✂️ DIY Opportunities:", "color": "#388e3c"},
            "setup_tips": {"label": "💡 Setup Tips:", "style": "info_card"},
        },
    },
    "menu_options": {
        "title": "🍽️ Menu Options",
        "color": "#ff6f00",
        "icon": "mi:restaurant",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "menu",
    },
    "activities": {
        "title": "🎮 Activities",
        "color": "#9c27b0",
        "icon": "mi:sports_esports",
        "initially_open": True,
        "renderer": "card_list",
        "card_type": "activity",
    },
    "timeline": {
        "title": "⏰ Event Timeline",
        "color": "#1976d2",
        "icon": "mi:schedule",
        "initially_open": True,
        "renderer": "timeline",
    },
    "budget_breakdown": {
        "title": "💰 Budget Breakdown",
        "color": "#4caf50",
        "icon": "mi:account_balance_wallet",
        "initially_open": True,
        "renderer": "budget",
    },
    "special_touches": {
        "title": "✨ Special Touches",
        "color": "#ffd700",
        "icon": "mi:star",
        "initially_open": False,
        "renderer": "simple_list",
    },
    # Professional Gathering sections
    "agenda": {
        "title": "📋 Agenda",
        "color": "#1976d2",
        "icon": "mi:list_alt",
        "initially_open": True,
        "renderer": "card_list",
        "card_type": "generic",
    },
    "networking_approach": {
        "title": "🤝 Networking",
        "color": "#388e3c",
        "icon": "mi:groups",
        "initially_open": False,
        "renderer": "text",
    },
    "room_setup": {
        "title": "🏢 Room Setup",
        "color": "#ff9800",
        "icon": "mi:meeting_room",
        "initially_open": False,
        "renderer": "text",
    },
    "tech_needs": {
        "title": "💻 Tech Requirements",
        "color": "#f44336",
        "icon": "mi:computer",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "refreshments": {
        "title": "☕ Refreshments",
        "color": "#795548",
        "icon": "mi:local_cafe",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "materials": {
        "title": "📄 Materials",
        "color": "#607d8b",
        "icon": "mi:description",
        "initially_open": False,
        "renderer": "simple_list",
    },
    # Intellectual Gathering sections
    "discussion_format": {
        "title": "💬 Discussion Format",
        "color": "#7b1fa2",
        "icon": "mi:forum",
        "initially_open": True,
        "renderer": "text",
    },
    "preparation_guidelines": {
        "title": "📚 Preparation",
        "color": "#5e35b1",
        "icon": "mi:school",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "discussion_prompts": {
        "title": "💡 Discussion Prompts",
        "color": "#7b1fa2",
        "icon": "mi:lightbulb",
        "initially_open": True,
        "renderer": "numbered_list",
    },
    "seating_arrangement": {
        "title": "🪑 Seating",
        "color": "#388e3c",
        "icon": "mi:event_seat",
        "initially_open": False,
        "renderer": "text",
    },
    "materials_needed": {
        "title": "📖 Materials",
        "color": "#e64a19",
        "icon": "mi:book",
        "initially_open": False,
        "renderer": "simple_list",
    },
    # Common sections
    "logistics": {
        "title": "Logistics",
        "color": "#3f51b5",
        "icon": "mi:local_shipping",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "contingency_notes": {
        "title": "Contingency Plans",
        "color": "#f44336",
        "icon": "mi:security",
        "initially_open": False,
        "renderer": "simple_list",
    },
    "reasoning": {
        "title": "💭 AI Reasoning",
        "color": "#9c27b0",
        "icon": "mi:psychology",
        "initially_open": False,
        "renderer": "text",
    },
}

# Card type configurations
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
    "generic": {
        "fields": [
            {"key": "*", "type": "auto"}  # Auto-detect all fields
        ]
    },
}

# ============================================================================
# MAIN BUILDER
# ============================================================================


# ============================================================================
# SELECTION STATE
# ============================================================================

# Global selection state (scoped to this module)
_selected_options = {}


def get_selected_options():
    """Get all selected options"""
    return _selected_options.copy()


def clear_selections():
    """Clear all selections"""
    global _selected_options
    _selected_options = {}


# ============================================================================
# CONFIGURATION
# ============================================================================

SECTION_CONFIG = {
    "themes": {
        "title": "🎨 Theme Options",
        "color": "#673ab7",
        "icon": "mi:palette",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "theme",
        "selectable": True,  # NEW: Enable selection
        "selection_label": "Theme",
    },
    "decorations": {
        "title": "🎈 Decorations",
        "color": "#e91e63",
        "icon": "mi:celebration",
        "initially_open": True,
        "renderer": "structured_list",
        "subsections": {
            "essential_items": {"label": "🔴 Essential Items:", "color": "#d32f2f"},
            "optional_items": {"label": "🔵 Optional Items:", "color": "#1976d2"},
            "diy_opportunities": {"label": "✂️ DIY Opportunities:", "color": "#388e3c"},
            "setup_tips": {"label": "💡 Setup Tips:", "style": "info_card"},
        },
        "selectable": False,  # Not selectable - just informational
    },
    "menu_options": {
        "title": "🍽️ Menu Options",
        "color": "#ff6f00",
        "icon": "mi:restaurant",
        "initially_open": False,
        "renderer": "card_list",
        "card_type": "menu",
        "selectable": True,  # NEW: Enable selection
        "selection_label": "Menu",
    },
    "activities": {
        "title": "🎮 Activities",
        "color": "#9c27b0",
        "icon": "mi:sports_esports",
        "initially_open": True,
        "renderer": "card_list",
        "card_type": "activity",
        "selectable": True,  # NEW: Enable multi-selection
        "selection_label": "Activity",
        "multi_select": True,  # Allow selecting multiple activities
    },
    "timeline": {
        "title": "⏰ Event Timeline",
        "color": "#1976d2",
        "icon": "mi:schedule",
        "initially_open": True,
        "renderer": "timeline",
        "selectable": False,  # Timeline is saved automatically
        "save_to_table": True,  # Will be saved to tasks table
    },
    "budget_breakdown": {
        "title": "💰 Budget Breakdown",
        "color": "#4caf50",
        "icon": "mi:account_balance_wallet",
        "initially_open": True,
        "renderer": "budget",
        "selectable": False,  # Budget is saved automatically
        "save_to_table": True,  # Will be saved to budget_items table
    },
    "special_touches": {
        "title": "✨ Special Touches",
        "color": "#ffd700",
        "icon": "mi:star",
        "initially_open": False,
        "renderer": "simple_list",
        "selectable": True,
        "selection_label": "Special Touch",
        "multi_select": True,
    },
    # ... rest of config stays the same
}

# ============================================================================
# MAIN BUILDER
# ============================================================================


def build_event_plan_ui(event_plan_data, container):
    """
    Build complete UI for EventPlan response with selection support
    """

    # Clear previous selections
    clear_selections()

    # Add header
    add_plan_header(container, event_plan_data)

    # Key Considerations
    if "key_considerations" in event_plan_data:
        add_key_considerations(container, event_plan_data["key_considerations"])

    # Process main plan section
    if "plan" in event_plan_data:
        render_plan_sections(container, event_plan_data["plan"])

    # Process root-level sections
    for key in ["logistics", "contingency_notes", "reasoning"]:
        if key in event_plan_data:
            render_section(container, key, event_plan_data[key])

    # Add save button at the bottom
    add_save_button(container, event_plan_data)


# ============================================================================
# SELECTION-ENABLED RENDERERS
# ============================================================================


def render_card_list_section(container, section_key, items, config):
    """Render section with list of cards - now with selection support"""

    if not isinstance(items, list):
        items = [items]

    # Get card type config
    card_type = config.get("card_type", "generic")
    card_config = CARD_TYPES.get(card_type, CARD_TYPES["generic"])

    # Check if selectable
    is_selectable = config.get("selectable", False)
    is_multi_select = config.get("multi_select", False)
    selection_label = config.get("selection_label", "Option")

    # Create accordion
    accordion = create_accordion_container(config, len(items))
    header_container, header_btn, content_panel = accordion

    # Add selection instruction if selectable
    if is_selectable:
        instruction_text = f"Select {'one or more' if is_multi_select else 'one'} {selection_label.lower()}:"
        content_panel.add_component(
            Label(
                text=instruction_text,
                font_size=12,
                italic=True,
                foreground="#666",
                spacing_above="small",
                spacing_below="small",
            )
        )

    # Create cards with selection
    for i, item in enumerate(items, 1):
        if is_selectable:
            card = create_selectable_card(
                item, i, card_config, section_key, selection_label, is_multi_select
            )
        else:
            card = create_configured_card(item, i, card_config)

        content_panel.add_component(card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def create_selectable_card(
    item, index, card_config, section_key, selection_label, is_multi_select
):
    """Create a card with selection capability"""

    # Outer container for selection state
    card_container = ColumnPanel(spacing_above="small", spacing_below="none")

    # Card itself
    card = m3.Card(appearance="outlined")
    card_content = m3.CardContentContainer(margin="16px")

    # Selection control (Radio or Checkbox)
    selection_control = None

    if is_multi_select:
        # Checkbox for multi-select
        selection_control = CheckBox(
            text=f"{selection_label} #{index}", bold=True, font_size=14, checked=False
        )
    else:
        # Radio button for single select
        selection_control = m3.RadioButton(
            text=f"{selection_label} #{index}",
            group_name=section_key,
            value=f"{section_key}_{index}",
            bold=True,
            font_size=14,
        )

    card_content.add_component(selection_control)

    # Card title (if configured)
    title_key = card_config.get("title_key")
    if title_key and title_key in item:
        card_content.add_component(
            Label(
                text=item[title_key],
                font_size=15,
                bold=True,
                foreground="#673ab7",
                spacing_above="small",
            )
        )

    # Card fields
    fields = card_config.get("fields", [])
    for field in fields:
        key = field["key"]

        if key == "*":
            for k, v in item.items():
                if k != title_key:
                    render_field(card_content, k, v, {"type": "auto"})
            continue

        if key not in item:
            continue

        if field.get("skip_if_empty") and not item[key]:
            continue

        render_field(card_content, key, item[key], field)

    card.add_component(card_content)
    card_container.add_component(card)

    # Selection handler
    def on_selection_changed(**event_args):
        if is_multi_select:
            # Checkbox - add/remove from selections
            if selection_control.checked:
                if section_key not in _selected_options:
                    _selected_options[section_key] = []
                if item not in _selected_options[section_key]:
                    _selected_options[section_key].append(item)
                card.appearance = "filled"
            else:
                if (
                    section_key in _selected_options
                    and item in _selected_options[section_key]
                ):
                    _selected_options[section_key].remove(item)
                card.appearance = "outlined"
        else:
            # Radio button - single selection
            if selection_control.selected:
                _selected_options[section_key] = item
                # Highlight selected card
                card.appearance = "filled"

                # Unhighlight others (find siblings)
                parent = card_container.parent
                for sibling in parent.get_components():
                    if sibling != card_container:
                        for child in sibling.get_components():
                            if isinstance(child, m3.Card):
                                child.appearance = "outlined"

    if is_multi_select:
        selection_control.set_event_handler("change", on_selection_changed)
    else:
        selection_control.set_event_handler("x-change", on_selection_changed)

    return card_container


# ============================================================================
# SAVE FUNCTIONALITY
# ============================================================================


def add_save_button(container, event_plan_data):
    """Add save button at the bottom"""

    button_panel = LinearPanel(
        spacing="medium",
        spacing_above="large",
        spacing_below="medium",
        align="center",
    )

    # Selection summary
    summary_label = Label(
        text="Select your preferred options above, then click Save",
        font_size=13,
        italic=True,
        foreground="#666",
    )
    button_panel.add_component(summary_label)

    # Save button
    save_btn = m3.Button(
        text="💾 Save Selections", icon="mi:save", appearance="filled", size="large"
    )
    save_btn.tag.event_plan_data = event_plan_data  # Store full plan data

    def on_save_click(**event_args):
        save_selections(save_btn, event_plan_data)

    save_btn.set_event_handler("click", on_save_click)
    button_panel.add_component(save_btn)

    container.add_component(button_panel)


def save_selections(save_btn, event_plan_data):
    """Save selected options and all data to database"""

    # Get selections
    selections = get_selected_options()

    # Validate - check if user made selections
    selectable_sections = [
        key for key, config in SECTION_CONFIG.items() if config.get("selectable", False)
    ]

    # Check if at least one selection was made
    if not selections:
        alert("Please select at least one option before saving", title="No Selections")
        return

    # Show missing selections warning
    missing = [
        format_title(key)
        for key in selectable_sections
        if key not in selections and not SECTION_CONFIG[key].get("multi_select")
    ]

    if missing:
        confirm_msg = (
            f"You haven't selected: {', '.join(missing)}.\n\nDo you want to continue?"
        )
        if not confirm(confirm_msg, title="Incomplete Selection"):
            return

    # Prepare data for server
    save_data = {
        "selected_options": selections,
        "timeline": event_plan_data.get("plan", {}).get("timeline", []),
        "budget_breakdown": event_plan_data.get("plan", {}).get("budget_breakdown", []),
        "full_plan": event_plan_data,  # Include full plan for reference
    }

    # Disable button and show loading
    save_btn.enabled = False
    save_btn.text = "⏳ Saving..."

    try:
        # Call server function
        result = anvil.server.call("save_event_selections", save_data)

        if result["success"]:
            # Success notification
            Notification(
                f"✅ Saved! {result.get('tasks_saved', 0)} tasks, {result.get('budget_items_saved', 0)} budget items",
                timeout=5,
                style="success",
            ).show()

            # Navigate to event view
            event_id = result.get("event_id")
            if event_id:
                from ... import Events

                open_form("Events.EventView", event_id=event_id)
        else:
            alert(
                f"Error saving selections:\n{result.get('error')}", title="Save Failed"
            )
            save_btn.enabled = True
            save_btn.text = "💾 Save Selections"

    except Exception as e:
        print(f"Error saving selections: {e}")
        alert(f"An error occurred:\n{str(e)}", title="Save Failed")
        save_btn.enabled = True
        save_btn.text = "💾 Save Selections"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def format_title(text):
    """Format key to title"""
    return text.replace("_", " ").title()


# ... rest of the code remains the same (all the renderer functions, etc.)


def render_plan_sections(container, plan_data):
    """
    Render all sections in the plan based on configuration

    Args:
        container: Parent container
        plan_data: Plan dict (contains event_type and sections)
    """

    # Iterate through all keys in plan_data
    for key, value in plan_data.items():
        if key == "event_type":
            continue  # Skip event_type discriminator

        # Render section if it has a configuration
        if key in SECTION_CONFIG:
            render_section(container, key, value)
        else:
            # Fallback: auto-detect rendering
            render_generic_section(container, key, value)


def render_section(container, section_key, content):
    """
    Render a section based on its configuration

    Args:
        container: Parent container
        section_key: Key in SECTION_CONFIG
        content: Content to render
    """

    config = SECTION_CONFIG.get(section_key)
    if not config:
        # No config - use generic rendering
        render_generic_section(container, section_key, content)
        return

    # Get renderer type
    renderer = config.get("renderer", "auto")

    # Route to appropriate renderer
    if renderer == "card_list":
        render_card_list_section(container, section_key, content, config)
    elif renderer == "simple_list":
        render_simple_list_section(container, section_key, content, config)
    elif renderer == "numbered_list":
        render_numbered_list_section(container, section_key, content, config)
    elif renderer == "text":
        render_text_section(container, section_key, content, config)
    elif renderer == "timeline":
        render_timeline_section(container, section_key, content, config)
    elif renderer == "budget":
        render_budget_section(container, section_key, content, config)
    elif renderer == "structured_list":
        render_structured_list_section(container, section_key, content, config)
    else:
        # Auto-detect
        render_generic_section(container, section_key, content)


# ============================================================================
# SECTION RENDERERS
# ============================================================================


def render_simple_list_section(container, section_key, items, config):
    """Render simple bullet list"""

    accordion = create_accordion_container(
        config, len(items) if isinstance(items, list) else None
    )
    header_container, header_btn, content_panel = accordion

    # Handle different content types
    if isinstance(items, list):
        for item in items:
            bullet = create_bullet_item(item)
            content_panel.add_component(bullet)
    else:
        content_panel.add_component(Label(text=str(items), font_size=13))

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def render_numbered_list_section(container, section_key, items, config):
    """Render numbered list in cards"""

    accordion = create_accordion_container(
        config, len(items) if isinstance(items, list) else None
    )
    header_container, header_btn, content_panel = accordion

    if isinstance(items, list):
        for i, item in enumerate(items, 1):
            card = m3.Card(appearance="outlined", spacing_above="small")
            card_content = m3.CardContentContainer(margin="12px")
            card_content.add_component(Label(text=f"{i}. {item}", font_size=13))
            card.add_component(card_content)
            content_panel.add_component(card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def render_text_section(container, section_key, text, config):
    """Render simple text content"""

    accordion = create_accordion_container(config)
    header_container, header_btn, content_panel = accordion

    content_panel.add_component(Label(text=str(text), font_size=13))

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def render_timeline_section(container, section_key, timeline_items, config):
    """Render timeline with alternating cards"""

    accordion = create_accordion_container(config, len(timeline_items))
    header_container, header_btn, content_panel = accordion

    for i, item in enumerate(timeline_items):
        timeline_card = m3.Card(
            appearance="filled" if i % 2 == 0 else "outlined", spacing_above="small"
        )
        timeline_content = m3.CardContentContainer(margin="12px")

        # Time and activity
        time_panel = FlowPanel(spacing="small")
        time_panel.add_component(
            Label(
                text=item.get("time", ""),
                font_size=14,
                bold=True,
                foreground=config.get("color", "#1976d2"),
            )
        )
        time_panel.add_component(Label(text=item.get("activity", ""), font_size=13))
        timeline_content.add_component(time_panel)

        # Responsible party (if present)
        if "responsible_party" in item and item["responsible_party"]:
            timeline_content.add_component(
                Label(
                    text=f"👤 {item['responsible_party']}",
                    font_size=11,
                    foreground="#666",
                    italic=True,
                    spacing_above="tiny",
                )
            )

        timeline_card.add_component(timeline_content)
        content_panel.add_component(timeline_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def render_budget_section(container, section_key, budget_items, config):
    """Render budget with progress bars"""

    accordion = create_accordion_container(config, len(budget_items))
    header_container, header_btn, content_panel = accordion

    # Total card
    total = sum(item["amount"] for item in budget_items)
    total_card = m3.Card(appearance="filled", spacing_above="small")
    total_content = m3.CardContentContainer(margin="12px")
    total_content.add_component(
        Label(
            text=f"Total Budget: ${total:,.2f}",
            font_size=18,
            bold=True,
            foreground="#2e7d32",
        )
    )
    total_card.add_component(total_content)
    content_panel.add_component(total_card)

    # Budget item cards
    for item in budget_items:
        budget_card = create_budget_card(item)
        content_panel.add_component(budget_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def render_structured_list_section(container, section_key, content_dict, config):
    """Render structured content with subsections (e.g., decorations)"""

    accordion = create_accordion_container(config)
    header_container, header_btn, content_panel = accordion

    subsections = config.get("subsections", {})

    for key, value in content_dict.items():
        if key not in subsections:
            continue

        subsection_config = subsections[key]
        label_text = subsection_config.get("label", format_title(key))

        # Subsection header
        content_panel.add_component(
            Label(
                text=label_text,
                bold=True,
                font_size=14,
                foreground=subsection_config.get("color", "#000"),
                spacing_above="small",
            )
        )

        # Subsection content
        if subsection_config.get("style") == "info_card":
            # Special info card
            info_card = m3.Card(appearance="filled", spacing_above="small")
            info_content = m3.CardContentContainer(margin="12px")
            info_content.add_component(Label(text=str(value), font_size=12))
            info_card.add_component(info_content)
            content_panel.add_component(info_card)
        elif isinstance(value, list):
            # Bullet list
            for item in value:
                bullet = create_bullet_item(item, color=subsection_config.get("color"))
                content_panel.add_component(bullet)
        else:
            # Plain text
            content_panel.add_component(Label(text=str(value), font_size=13))

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)

    container.add_component(header_container, full_width_row=True)
    container.add_component(card_content)


def render_generic_section(container, section_key, content):
    """Fallback generic renderer - auto-detect content type"""

    # Create default config
    default_config = {
        "title": format_title(section_key),
        "color": "#2196f3",
        "initially_open": False,
    }

    # Auto-detect and render
    if isinstance(content, list):
        render_simple_list_section(container, section_key, content, default_config)
    elif isinstance(content, dict):
        # Render as key-value pairs
        accordion = create_accordion_container(default_config)
        header_container, header_btn, content_panel = accordion

        for key, value in content.items():
            row = create_key_value_row(key, value)
            content_panel.add_component(row)

        card_content = m3.CardContentContainer(margin="16px")
        card_content.add_component(content_panel)

        container.add_component(header_container, full_width_row=True)
        container.add_component(card_content)
    else:
        # Simple text
        render_text_section(container, section_key, content, default_config)


# ============================================================================
# REUSABLE COMPONENTS
# ============================================================================


def create_accordion_container(config, item_count=None):
    """
    Create accordion header and content panel with toggle
    Returns: (header_container, header_btn, content_panel)
    """

    title = config.get("title", "Section")
    color = config.get("color", "#2196f3")
    initially_open = config.get("initially_open", False)

    # Add count to title if provided
    if item_count is not None:
        title = f"{title} ({item_count} items)"

    # Header container
    header_container = ColumnPanel(
        background="theme:Surface Variant"
        if initially_open
        else "theme:Surface Container",
        spacing_above="none",
        spacing_below="none",
    )

    # Header button
    header_btn = m3.Link(
        text=title,
        align="left",
        icon="mi:arrow_drop_down" if initially_open else "mi:arrow_right",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        foreground=color,
    )

    if initially_open:
        header_btn.background = "theme:Surface Variant"
        header_btn.role = "filled-button"

    header_container.add_component(header_btn)

    # Content panel
    content_panel = ColumnPanel(
        visible=initially_open, spacing_above="none", spacing_below="none"
    )

    # Toggle functionality
    is_expanded = {"value": initially_open}

    def toggle(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        header_btn.icon = (
            "mi:arrow_drop_down" if is_expanded["value"] else "mi:arrow_right"
        )

        if is_expanded["value"]:
            header_btn.background = "theme:Surface Variant"
            header_btn.role = "filled-button"
        else:
            header_btn.background = ""
            header_btn.role = None

    header_btn.set_event_handler("click", toggle)

    return (header_container, header_btn, content_panel)


def create_configured_card(item, index, card_config):
    """
    Create card based on card configuration

    Args:
        item: Dict with item data
        index: Item number
        card_config: Card type configuration
    """

    card = m3.Card(appearance="outlined", spacing_above="small")
    card_content = m3.CardContentContainer(margin="16px")

    # Card title (if configured)
    title_key = card_config.get("title_key")
    if title_key and title_key in item:
        card_content.add_component(
            Label(
                text=f"#{index}: {item[title_key]}",
                font_size=16,
                bold=True,
                foreground="#673ab7",
            )
        )

    # Card fields
    fields = card_config.get("fields", [])

    for field in fields:
        key = field["key"]
        field_type = field["type"]

        # Handle wildcard (all fields)
        if key == "*":
            for k, v in item.items():
                if k != title_key:  # Skip title key
                    render_field(card_content, k, v, {"type": "auto"})
            continue

        # Skip if field not in item
        if key not in item:
            continue

        # Skip if empty and skip_if_empty flag set
        if field.get("skip_if_empty") and not item[key]:
            continue

        # Render field
        render_field(card_content, key, item[key], field)

    card.add_component(card_content)
    return card


def render_field(container, key, value, field_config):
    """Render a single field based on its type"""

    field_type = field_config.get("type", "auto")

    # Auto-detect type
    if field_type == "auto":
        if isinstance(value, list):
            field_type = "bullet_list"
        else:
            field_type = "text"

    # Render based on type
    if field_type == "text":
        label = Label(text=str(value), font_size=13, spacing_above="small")
        if field_config.get("italic"):
            label.italic = True
        container.add_component(label)

    elif field_type == "inline":
        # Inline with prefix (e.g., "⏱️ 30 minutes")
        prefix = field_config.get("prefix", "")
        container.add_component(
            Label(
                text=f"{prefix} {value}",
                font_size=12,
                foreground="#666",
                spacing_above="small",
            )
        )

    elif field_type == "key_value":
        row = FlowPanel(spacing="tiny", spacing_above="small")
        row.add_component(Label(text=f"{format_title(key)}:", bold=True, font_size=12))
        row.add_component(Label(text=str(value), font_size=12))
        container.add_component(row)

    elif field_type == "bullet_list":
        # List label
        if "label" in field_config:
            container.add_component(
                Label(
                    text=field_config["label"],
                    bold=True,
                    font_size=12,
                    spacing_above="small",
                )
            )

        # List items
        for item in value:
            bullet = create_bullet_item(item)
            container.add_component(bullet)

    elif field_type == "color_palette":
        # Special color palette rendering
        colors_panel = FlowPanel(spacing="small", spacing_above="small")
        colors_panel.add_component(Label(text="Colors:", bold=True, font_size=12))

        for color in value:
            color_value = (
                color
                if color.startswith("#")
                else f"#{color}"
                if len(color) == 6
                else color
            )
            color_box = Label(
                text="    ", background=color_value, border="1px solid #ccc"
            )
            colors_panel.add_component(color_box)
            colors_panel.add_component(Label(text=color, font_size=11))

        container.add_component(colors_panel)


def create_bullet_item(text, color=None):
    """Create a bullet point item"""
    bullet = FlowPanel(spacing="tiny")
    bullet_label = Label(text="  •", font_size=14)
    if color:
        bullet_label.foreground = color
    bullet.add_component(bullet_label)
    bullet.add_component(Label(text=str(text), font_size=13))
    return bullet


def create_key_value_row(key, value):
    """Create key-value row"""
    row = FlowPanel(spacing="tiny", spacing_above="tiny")
    row.add_component(Label(text=f"{format_title(key)}:", bold=True, font_size=12))
    row.add_component(Label(text=str(value), font_size=12))
    return row


def create_budget_card(item):
    """Create budget item card with progress bar"""
    card = m3.Card(appearance="outlined", spacing_above="small")
    card_content = m3.CardContentContainer(margin="12px")

    # Header
    header = FlowPanel(spacing="small")
    header.add_component(Label(text=item["category"], font_size=14, bold=True))
    header.add_component(
        Label(
            text=f"${item['amount']:,.2f}",
            font_size=14,
            bold=True,
            foreground="#4caf50",
        )
    )
    card_content.add_component(header)

    # Percentage
    percentage = item["percentage"]
    card_content.add_component(
        Label(
            text=f"{percentage:.1f}% of total budget",
            font_size=12,
            foreground="#666",
            spacing_above="tiny",
        )
    )

    # Progress bar
    bar_container = ColumnPanel(background="#e0e0e0", spacing_above="small")
    bar_fill = Label(text="  ", background="#4caf50")
    bar_container.add_component(bar_fill)
    card_content.add_component(bar_container)

    # Notes
    if "notes" in item and item["notes"]:
        card_content.add_component(
            Label(
                text=f"💡 {item['notes']}",
                font_size=11,
                italic=True,
                foreground="#666",
                spacing_above="small",
            )
        )

    card.add_component(card_content)
    return card


# ============================================================================
# SPECIAL SECTIONS (Not Configuration-Driven)
# ============================================================================


def add_plan_header(container, plan_data):
    """Add header with event classification"""
    header = ColumnPanel(
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        foreground="black",
        spacing="small",
    )

    title = Label(
        text="🎉 Event Options",
        font_size=20,
        bold=True,
        foreground="black",
        align="left",
    )
    header.add_component(title)
    container.add_component(header)


def add_key_considerations(container, considerations):
    """Add key considerations section (always expanded)"""
    section = m3.Card(appearance="outlined", spacing_above="small")
    card_content = m3.CardContentContainer(margin="16px")

    # Header
    card_content.add_component(
        Label(
            text="🎯 Key Considerations", font_size=18, bold=True, foreground="#2e7d32"
        )
    )

    # Items
    items_panel = ColumnPanel(spacing_above="none", spacing_below="none")
    for item in considerations:
        item_panel = FlowPanel(spacing_above="none", spacing_below="none")
        item_panel.add_component(
            Label(text="   ✓", foreground="#4caf50", font_size=16, bold=True)
        )
        item_panel.add_component(Label(text=item, font_size=14))
        items_panel.add_component(item_panel)

    card_content.add_component(items_panel)
    section.add_component(card_content)
    container.add_component(section)


def format_title(text):
    """Format key to title"""
    return text.replace("_", " ").title()

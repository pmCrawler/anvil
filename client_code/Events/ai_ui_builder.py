# ClientModules/ai_ui_builder.py

"""
Dynamic UI Builder for Event Planning AI Responses
Handles EventPlan structure with discriminated unions
"""

import anvil.server
from anvil import *

# ============================================================================
# MAIN BUILDER
# ============================================================================


def build_event_plan_ui(event_plan_data, container):
    """
    Build complete UI for EventPlan response

    Args:
        event_plan_data: Dict with EventPlan structure
        container: Anvil ColumnPanel to add components to
    """

    # Clear container
    container.clear()

    # Add header
    add_plan_header(container, event_plan_data)

    # Key Considerations (expanded by default)
    if "key_considerations" in event_plan_data:
        add_key_considerations(container, event_plan_data["key_considerations"])

    # Main Plan Section (based on event type)
    if "plan" in event_plan_data:
        add_plan_section(container, event_plan_data["plan"])

    # Logistics
    if "logistics" in event_plan_data:
        add_simple_list_section(
            container,
            "Logistics",
            event_plan_data["logistics"],
            icon="fa:truck",
            color="#3f51b5",
        )

    # Contingency Notes
    if "contingency_notes" in event_plan_data:
        add_simple_list_section(
            container,
            "Contingency Plans",
            event_plan_data["contingency_notes"],
            icon="fa:shield",
            color="#f44336",
        )

    # Reasoning
    if "reasoning" in event_plan_data:
        add_reasoning_section(container, event_plan_data["reasoning"])

    # Action Buttons
    add_action_buttons(container, event_plan_data)


# ============================================================================
# HEADER & KEY SECTIONS
# ============================================================================


def add_plan_header(container, plan_data):
    """Add header with event classification"""

    header = ColumnPanel(
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        foreground="white",
        spacing="small",
    )

    # Event Classification
    classification = plan_data.get("event_classification", "Unknown Event Type")

    title = Label(
        text=f"🎉 {classification}", font_size=20, bold=True, foreground="white"
    )
    header.add_component(title)

    subtitle = Label(
        text="AI-Generated Event Plan", font_size=14, foreground="white", italic=True
    )
    header.add_component(subtitle)

    container.add_component(header)


def add_key_considerations(container, considerations):
    """Add key considerations section (expanded by default)"""

    section = ColumnPanel(background="#e8f5e9", spacing="small", spacing_above="small")

    # Header
    header_label = Label(
        text="🎯 Key Considerations", font_size=16, bold=True, foreground="#2e7d32"
    )
    section.add_component(header_label)

    # List items
    for item in considerations:
        item_panel = LinearPanel(spacing="tiny")
        item_panel.add_component(Label(text="✓", foreground="#4caf50", font_size=14))
        item_panel.add_component(Label(text=item, font_size=13))
        section.add_component(item_panel)

    container.add_component(section)


def add_reasoning_section(container, reasoning):
    """Add AI reasoning section"""

    expander = create_expander("💭 AI Reasoning", initially_open=False)

    expander.add_component(Label(text=reasoning, font_size=13, italic=True))

    container.add_component(expander)


# ============================================================================
# MAIN PLAN SECTION (Handles Discriminated Union)
# ============================================================================


def add_plan_section(container, plan_data):
    """
    Add main plan section based on event_type
    Handles: social_celebration, professional_gathering, intellectual_gathering
    """

    event_type = plan_data.get("event_type")

    if event_type == "social_celebration":
        add_social_celebration_plan(container, plan_data)
    elif event_type == "professional_gathering":
        add_professional_gathering_plan(container, plan_data)
    elif event_type == "intellectual_gathering":
        add_intellectual_gathering_plan(container, plan_data)
    else:
        # Fallback - generic rendering
        add_generic_plan(container, plan_data)


# ============================================================================
# SOCIAL CELEBRATION PLAN
# ============================================================================


def add_social_celebration_plan(container, plan):
    """Render social celebration plan"""

    # Themes
    if "themes" in plan:
        add_themes_section(container, plan["themes"])

    # Decorations
    if "decorations" in plan:
        add_decorations_section(container, plan["decorations"])

    # Menu Options
    if "menu_options" in plan:
        add_menu_options_section(container, plan["menu_options"])

    # Activities
    if "activities" in plan:
        add_activities_section(container, plan["activities"])

    # Timeline
    if "timeline" in plan:
        add_timeline_section(container, plan["timeline"])

    # Budget Breakdown
    if "budget_breakdown" in plan:
        add_budget_breakdown_section(container, plan["budget_breakdown"])

    # Special Touches
    if "special_touches" in plan:
        add_simple_list_section(
            container,
            "Special Touches",
            plan["special_touches"],
            icon="fa:star",
            color="#ffd700",
        )


def add_themes_section(container, themes):
    """Render theme options"""

    expander = create_expander(
        f"🎨 Theme Options ({len(themes)} options)", initially_open=True
    )

    for i, theme in enumerate(themes, 1):
        card = ColumnPanel(
            background="white",
            border="1px solid #e0e0e0",
            spacing="small",
            spacing_above="small",
        )

        # Theme name
        card.add_component(
            Label(
                text=f"#{i}: {theme['name']}",
                font_size=16,
                bold=True,
                foreground="#673ab7",
            )
        )

        # Description
        card.add_component(Label(text=theme["description"], font_size=13))

        # Color palette
        if "color_palette" in theme:
            colors_panel = LinearPanel(spacing="tiny")
            colors_panel.add_component(Label(text="Colors:", bold=True, font_size=12))

            for color in theme["color_palette"]:
                color_box = Label(
                    text="  ",
                    background=color if color.startswith("#") else f"#{color}",
                    border="1px solid #ccc",
                )
                colors_panel.add_component(color_box)
                colors_panel.add_component(Label(text=color, font_size=11))

            card.add_component(colors_panel)

        # Atmosphere
        if "atmosphere" in theme:
            atm_panel = LinearPanel(spacing="tiny")
            atm_panel.add_component(Label(text="Atmosphere:", bold=True, font_size=12))
            atm_panel.add_component(Label(text=theme["atmosphere"], font_size=12))
            card.add_component(atm_panel)

        # expander.add_component(card)
        expander.add_component(card)

    container.add_component(expander)


def add_decorations_section(container, decorations):
    """Render decorations plan"""

    expander = create_expander("🎈 Decorations", initially_open=True)

    # Essential items
    if "essential_items" in decorations:
        expander.add_component(
            Label(
                text="Essential Items:", bold=True, font_size=14, foreground="#d32f2f"
            )
        )
        for item in decorations["essential_items"]:
            expander.add_component(create_bullet_item(item, "🔴"))

    # Optional items
    if "optional_items" in decorations and decorations["optional_items"]:
        expander.add_component(
            Label(
                text="Optional Items:",
                bold=True,
                font_size=14,
                foreground="#1976d2",
                spacing_above="small",
            )
        )
        for item in decorations["optional_items"]:
            expander.add_component(create_bullet_item(item, "🔵"))

    # DIY opportunities
    if "diy_opportunities" in decorations and decorations["diy_opportunities"]:
        expander.add_component(
            Label(
                text="DIY Opportunities:",
                bold=True,
                font_size=14,
                foreground="#388e3c",
                spacing_above="small",
            )
        )
        for item in decorations["diy_opportunities"]:
            expander.add_component(create_bullet_item(item, "✂️"))

    # Setup tips
    if "setup_tips" in decorations:
        tip_card = ColumnPanel(
            background="#fff3e0", spacing="small", spacing_above="small"
        )
        tip_card.add_component(Label(text="💡 Setup Tips:", bold=True, font_size=13))
        tip_card.add_component(Label(text=decorations["setup_tips"], font_size=12))
        expander.add_component(tip_card)

    container.add_component(expander)


def add_menu_options_section(container, menu_options):
    """Render menu options"""

    expander = create_expander(
        f"🍽️ Menu Options ({len(menu_options)} options)", initially_open=True
    )

    for i, menu in enumerate(menu_options, 1):
        card = ColumnPanel(
            background="white",
            border="1px solid #e0e0e0",
            spacing="small",
            spacing_above="small",
        )

        # Style header
        card.add_component(
            Label(
                text=f"Option {i}: {menu['style']}",
                font_size=15,
                bold=True,
                foreground="#ff6f00",
            )
        )

        # Food items
        if "items" in menu:
            card.add_component(Label(text="Menu Items:", bold=True, font_size=12))
            for item in menu["items"]:
                card.add_component(create_bullet_item(item))

        # Dietary accommodations
        if "dietary_accommodations" in menu and menu["dietary_accommodations"]:
            card.add_component(
                Label(
                    text="Dietary Accommodations:",
                    bold=True,
                    font_size=12,
                    spacing_above="tiny",
                )
            )
            for item in menu["dietary_accommodations"]:
                card.add_component(create_bullet_item(item, "🌱"))

        # Beverage pairings
        if "beverage_pairings" in menu:
            card.add_component(
                Label(text="Beverages:", bold=True, font_size=12, spacing_above="tiny")
            )
            for item in menu["beverage_pairings"]:
                card.add_component(create_bullet_item(item, "🥤"))

        expander.add_component(card)

    container.add_component(expander)


def add_activities_section(container, activities):
    """Render activities/entertainment"""

    expander = create_expander(
        f"🎮 Activities ({len(activities)} activities)", initially_open=True
    )

    for i, activity in enumerate(activities, 1):
        card = ColumnPanel(
            background="#f3e5f5",
            border="1px solid #9c27b0",
            spacing="small",
            spacing_above="small",
        )

        # Activity name and duration
        header = LinearPanel(spacing="small")
        header.add_component(
            Label(text=f"{i}. {activity['name']}", font_size=15, bold=True)
        )
        header.add_component(
            Label(text=f"⏱️ {activity['duration']}", font_size=12, foreground="#666")
        )
        card.add_component(header)

        # Instructions
        if "instructions" in activity:
            card.add_component(
                Label(text=activity["instructions"], font_size=12, italic=True)
            )

        # Materials needed
        if "materials_needed" in activity and activity["materials_needed"]:
            card.add_component(
                Label(
                    text="Materials needed:",
                    bold=True,
                    font_size=12,
                    spacing_above="tiny",
                )
            )
            for material in activity["materials_needed"]:
                card.add_component(create_bullet_item(material, "📦"))

        expander.add_component(card)

    container.add_component(expander)


def add_timeline_section(container, timeline):
    """Render event timeline"""

    expander = create_expander(
        f"⏰ Event Timeline ({len(timeline)} items)", initially_open=True
    )

    for i, item in enumerate(timeline):
        timeline_card = LinearPanel(
            background="white" if i % 2 == 0 else "#f5f5f5",
            spacing="small",
            spacing_above="tiny",
        )

        # Time
        timeline_card.add_component(
            Label(
                text=item["time"],
                font_size=14,
                bold=True,
                foreground="#1976d2",
                width=120,
            )
        )

        # Activity
        activity_panel = ColumnPanel(spacing="tiny")
        activity_panel.add_component(Label(text=item["activity"], font_size=13))

        # Responsible party
        if "responsible_party" in item and item["responsible_party"]:
            activity_panel.add_component(
                Label(
                    text=f"👤 {item['responsible_party']}",
                    font_size=11,
                    foreground="#666",
                    italic=True,
                )
            )

        timeline_card.add_component(activity_panel)
        expander.add_component(timeline_card)

    container.add_component(expander)


# ============================================================================
# PROFESSIONAL GATHERING PLAN
# ============================================================================


def add_professional_gathering_plan(container, plan):
    """Render professional gathering plan"""

    # Agenda
    if "agenda" in plan:
        add_agenda_section(container, plan["agenda"])

    # Networking Approach
    if "networking_approach" in plan:
        add_info_card(
            container, "🤝 Networking Approach", plan["networking_approach"], "#1976d2"
        )

    # Room Setup
    if "room_setup" in plan:
        add_info_card(container, "🏢 Room Setup", plan["room_setup"], "#388e3c")

    # Tech Needs
    if "tech_needs" in plan:
        add_simple_list_section(
            container,
            "Technical Requirements",
            plan["tech_needs"],
            icon="fa:laptop",
            color="#ff9800",
        )

    # Refreshments
    if "refreshments" in plan:
        add_simple_list_section(
            container,
            "Refreshments",
            plan["refreshments"],
            icon="fa:coffee",
            color="#795548",
        )

    # Materials
    if "materials" in plan:
        add_simple_list_section(
            container,
            "Materials & Handouts",
            plan["materials"],
            icon="fa:file-text",
            color="#607d8b",
        )

    # Budget
    if "budget_breakdown" in plan:
        add_budget_breakdown_section(container, plan["budget_breakdown"])


def add_agenda_section(container, agenda):
    """Render meeting agenda"""

    expander = create_expander(f"📋 Agenda ({len(agenda)} items)", initially_open=True)

    for i, item in enumerate(agenda, 1):
        agenda_card = ColumnPanel(
            background="white",
            border="1px solid #e0e0e0",
            spacing="small",
            spacing_above="small",
        )

        # Render dict items
        for key, value in item.items():
            if isinstance(value, list):
                agenda_card.add_component(
                    Label(text=f"{format_key(key)}:", bold=True, font_size=12)
                )
                for sub_item in value:
                    agenda_card.add_component(create_bullet_item(sub_item))
            else:
                row = LinearPanel(spacing="tiny")
                row.add_component(
                    Label(text=f"{format_key(key)}:", bold=True, font_size=12)
                )
                row.add_component(Label(text=str(value), font_size=12))
                agenda_card.add_component(row)

        expander.add_component(agenda_card)

    container.add_component(expander)


# ============================================================================
# INTELLECTUAL GATHERING PLAN
# ============================================================================


def add_intellectual_gathering_plan(container, plan):
    """Render intellectual gathering plan"""

    # Discussion Format
    if "discussion_format" in plan:
        add_info_card(
            container, "💬 Discussion Format", plan["discussion_format"], "#7b1fa2"
        )

    # Preparation Guidelines
    if "preparation_guidelines" in plan:
        add_simple_list_section(
            container,
            "Preparation for Attendees",
            plan["preparation_guidelines"],
            icon="fa:book",
            color="#5e35b1",
        )

    # Discussion Prompts
    if "discussion_prompts" in plan:
        add_discussion_prompts_section(container, plan["discussion_prompts"])

    # Seating Arrangement
    if "seating_arrangement" in plan:
        add_info_card(
            container, "🪑 Seating Arrangement", plan["seating_arrangement"], "#388e3c"
        )

    # Refreshments
    if "refreshments" in plan:
        add_simple_list_section(
            container,
            "Refreshments",
            plan["refreshments"],
            icon="fa:coffee",
            color="#795548",
        )

    # Materials
    if "materials_needed" in plan:
        add_simple_list_section(
            container,
            "Materials Needed",
            plan["materials_needed"],
            icon="fa:bookmark",
            color="#e64a19",
        )

    # Budget
    if "budget_breakdown" in plan:
        add_budget_breakdown_section(container, plan["budget_breakdown"])


def add_discussion_prompts_section(container, prompts):
    """Render discussion prompts"""

    expander = create_expander(
        f"💡 Discussion Prompts ({len(prompts)} prompts)", initially_open=True
    )

    for i, prompt in enumerate(prompts, 1):
        prompt_card = ColumnPanel(
            background="#ede7f6",
            border="1px solid #7b1fa2",
            spacing="small",
            spacing_above="small",
        )

        prompt_card.add_component(Label(text=f"{i}. {prompt}", font_size=13))

        expander.add_component(prompt_card)

    container.add_component(expander)


# ============================================================================
# BUDGET SECTION (Common to All Types)
# ============================================================================


def add_budget_breakdown_section(container, budget_items):
    """Render budget breakdown with visual bars"""

    expander = create_expander(
        f"💰 Budget Breakdown ({len(budget_items)} categories)", initially_open=True
    )

    # Calculate total
    total = sum(item["amount"] for item in budget_items)

    # Total card
    total_card = ColumnPanel(
        background="#fff3e0",
        spacing="small",
        spacing_above="none",
        spacing_below="small",
    )
    total_card.add_component(
        Label(
            text=f"Total Budget: ${total:,.2f}",
            font_size=16,
            bold=True,
            foreground="#e65100",
        )
    )
    expander.add_component(total_card)

    # Budget items
    for item in budget_items:
        budget_card = ColumnPanel(
            background="white",
            border="1px solid #e0e0e0",
            spacing="small",
            spacing_above="small",
        )

        # Header with category and amount
        header = LinearPanel(spacing="small")
        header.add_component(Label(text=item["category"], font_size=14, bold=True))
        header.add_component(
            Label(
                text=f"${item['amount']:,.2f}",
                font_size=14,
                bold=True,
                foreground="#4caf50",
            )
        )
        budget_card.add_component(header)

        # Percentage bar
        percentage = item["percentage"]
        bar_width = int(percentage)  # Simple percentage-based width

        bar_panel = LinearPanel(spacing="none", background="#e0e0e0")
        filled_bar = Label(
            text=f" {percentage:.1f}% ",
            background="#4caf50",
            foreground="white",
            font_size=11,
            bold=True,
        )
        bar_panel.add_component(filled_bar)
        budget_card.add_component(bar_panel)

        # Notes
        if "notes" in item and item["notes"]:
            budget_card.add_component(
                Label(
                    text=f"💡 {item['notes']}",
                    font_size=11,
                    italic=True,
                    foreground="#666",
                )
            )

        expander.add_component(budget_card)

    container.add_component(expander)


# ============================================================================
# HELPER COMPONENTS
# ============================================================================


def create_expander(title, badge=None, initially_open=False):
    """Create expandable section"""

    container = ColumnPanel(spacing="none")

    # Header
    header = LinearPanel(
        background="#f5f5f5",
        spacing="small",
        spacing_above="small",
        spacing_below="none",
    )

    # Title with icon
    icon_text = "▼ " if initially_open else "▶ "
    title_label = Label(text=f"{icon_text}{title}", font_size=15, bold=True)
    header.add_component(title_label)

    # Badge
    if badge:
        badge_label = Label(
            text=badge,
            font_size=11,
            background="#2196f3",
            foreground="white",
            bold=True,
        )
        header.add_component(badge_label)

    # Content
    content = ColumnPanel(visible=initially_open, spacing="small", background="#fafafa")

    # Toggle handler
    def toggle(**event_args):
        content.visible = not content.visible
        title_label.text = f"▼ {title}" if content.visible else f"▶ {title}"

    header.set_event_handler("x-click", toggle)

    # Assemble
    container.add_component(header)
    container.add_component(content)
    # container.content = content

    return container


def create_bullet_item(text, icon="•"):
    """Create bullet point item"""
    panel = LinearPanel(spacing="tiny")
    panel.add_component(Label(text=icon, font_size=12))
    panel.add_component(Label(text=text, font_size=12))
    return panel


def add_simple_list_section(container, title, items, icon="fa:list", color="#607d8b"):
    """Add simple list section"""

    expander = create_expander(f"{title} ({len(items)} items)", initially_open=False)

    for item in items:
        expander.add_component(create_bullet_item(item, "•"))

    container.add_component(expander)


def add_info_card(container, title, content, color="#2196f3"):
    """Add info card"""

    card = ColumnPanel(
        background="white",
        border=f"2px solid {color}",
        spacing="small",
        spacing_above="small",
    )

    card.add_component(Label(text=title, font_size=15, bold=True, foreground=color))

    card.add_component(Label(text=content, font_size=13))

    container.add_component(card)


def add_generic_plan(container, plan):
    """Generic renderer for unknown plan types"""

    for key, value in plan.items():
        if key == "event_type":
            continue

        if isinstance(value, list):
            add_simple_list_section(container, format_key(key), value)
        elif isinstance(value, dict):
            add_info_card(container, format_key(key), str(value))
        else:
            add_info_card(container, format_key(key), str(value))


def format_key(key):
    """Format key from snake_case to Title Case"""
    return key.replace("_", " ").title()


# ============================================================================
# ACTION BUTTONS
# ============================================================================


def add_action_buttons(container, event_plan_data):
    """Add action buttons"""

    button_panel = LinearPanel(
        spacing="small", spacing_above="medium", spacing_below="small"
    )

    # Save Plan button
    save_btn = Button(text="💾 Save Plan", icon="fa:save", role="primary-color")
    save_btn.tag.plan_data = event_plan_data
    button_panel.add_component(save_btn)

    # Export button
    export_btn = Button(text="📤 Export PDF", icon="fa:file-pdf-o")
    export_btn.tag.plan_data = event_plan_data
    button_panel.add_component(export_btn)

    # Share button
    share_btn = Button(text="🔗 Share", icon="fa:share-alt")
    button_panel.add_component(share_btn)

    container.add_component(button_panel)

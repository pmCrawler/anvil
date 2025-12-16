# ClientModules/ai_ui_builder.py

"""
Hybrid Dynamic UI Builder for Event Planning AI
Combines working accordion mechanics with color-coded, event-type-specific rendering
"""

from anvil import *
import anvil.server
import m3.components as m3

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
    # container.clear()

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
        create_accordion_section(
            container,
            "Logistics",
            event_plan_data["logistics"],
            icon="mi:local_shipping",
            color="#3f51b5",
            initially_open=False,
        )

    # Contingency Notes
    if "contingency_notes" in event_plan_data:
        create_accordion_section(
            container,
            "Contingency Plans",
            event_plan_data["contingency_notes"],
            icon="mi:security",
            color="#f44336",
            initially_open=False,
        )

    # Reasoning
    if "reasoning" in event_plan_data:
        add_reasoning_section(container, event_plan_data["reasoning"])


# ============================================================================
# ACCORDION COMPONENT (Working Implementation from AIResponse)
# ============================================================================


def create_accordion_section(
    container,
    title,
    content,
    icon="mi:arrow_right",
    color="#2196f3",
    initially_open=False,
):
    """
    Create working accordion section using m3 components

    Args:
        container: Parent container
        title: Section title
        content: Content (can be list, dict, or string)
        icon: Material icon name
        color: Color for the section
        initially_open: Whether to start expanded
    """

    # Main accordion container
    accordion = ColumnPanel(
        spacing_above="none",
        spacing_below="none",
    )

    # Card for content (initially hidden)
    card = m3.Card(appearance="outlined", visible=initially_open)

    # Content panel
    content_panel = ColumnPanel(
        visible=initially_open,
        spacing_above="none",
    )

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Container"
        if not initially_open
        else "theme:Surface Variant",
        spacing_above="small",
        spacing_below="small",
    )

    # Header button
    header_btn = m3.Link(
        text=format_title(title),
        align="left",
        icon="mi:arrow_drop_down" if initially_open else "mi:arrow_right",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        spacing="16px",
        foreground=color,
    )

    if initially_open:
        header_btn.background = "theme:Surface Variant"
        header_btn.role = "filled-button"

    header_container.add_component(header_btn)

    # Toggle functionality
    is_expanded = {"value": initially_open}

    def toggle_accordion(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        card.visible = is_expanded["value"]

        # Update icon
        header_btn.icon = (
            "mi:arrow_drop_down" if is_expanded["value"] else "mi:arrow_right"
        )

        # Update background
        if is_expanded["value"]:
            header_btn.background = "theme:Surface Variant"
            header_btn.role = "filled-button"
        else:
            header_btn.background = ""
            header_btn.role = None

    header_btn.set_event_handler("click", toggle_accordion)

    # Populate content based on type
    populate_content(content_panel, content)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)
    card.add_component(card_content)

    accordion.add_component(header_container, full_width_row=True)
    accordion.add_component(card)

    container.add_component(accordion)


def populate_content(content_panel, content):
    """Populate content panel based on content type"""

    if isinstance(content, str):
        # Simple text
        content_panel.add_component(
            Label(
                text=content,
                font_size=13,
            )
        )

    elif isinstance(content, list):
        # List of items
        for item in content:
            if isinstance(item, str):
                # Simple bullet point
                bullet_panel = FlowPanel(spacing="tiny")
                bullet_panel.add_component(Label(text="   •", font_size=14))
                bullet_panel.add_component(Label(text=item, font_size=13))
                content_panel.add_component(bullet_panel)
            else:
                # Complex item (dict)
                item_card = create_item_card(item)
                content_panel.add_component(item_card)

    elif isinstance(content, dict):
        # Dictionary
        for key, value in content.items():
            row = create_key_value_row(key, value)
            content_panel.add_component(row)


# ============================================================================
# HEADER & KEY SECTIONS
# ============================================================================


def add_plan_header(container, plan_data):
    """Add header with event classification"""

    header = ColumnPanel(
        background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        foreground="black",
        spacing="small",
    )

    # Event Classification
    # classification = plan_data.get("event_classification", "Unknown Event Type")

    title = Label(
        text="🎉 Event Options",
        font_size=20,
        bold=True,
        foreground="black",
        align="left",
    )
    header.add_component(title)
    container.add_component(header)
    # subtitle = Label(
    #     text="Event Options",
    #     font_size=14,
    #     foreground="black",
    #     italic=True,
    #     align="left",
    # )
    # header.add_component(subtitle)


def add_key_considerations(container, considerations):
    """Add key considerations section (expanded by default)"""

    section = m3.Card(
        appearance="outlined",
        spacing_above="small",
    )

    card_content = m3.CardContentContainer(margin="16px")

    # Header
    header_label = Label(
        text="🎯 Key Considerations", font_size=18, bold=True, foreground="#2e7d32"
    )
    card_content.add_component(header_label)

    # List items
    items_panel = ColumnPanel(
        # spacing="small",
        spacing_above="none",
        spacing_below="none",
    )
    for item in considerations:
        # item_panel = FlowPanel(spacing='small')
        # [H.E. 12/14] Use FlowPanel for icon and text on same line
        item_panel = FlowPanel(
            spacing_above="none",
            spacing_below="none",
        )
        item_panel.add_component(
            Label(
                text="   ✓",
                foreground="#4caf50",
                font_size=16,
                bold=True,
                spacing_above="none",
                spacing_below="none",
            )
        )
        item_panel.add_component(Label(text=item, font_size=14))
        items_panel.add_component(item_panel)

    card_content.add_component(items_panel)
    section.add_component(card_content)
    container.add_component(section)


def add_reasoning_section(container, reasoning):
    """Add AI reasoning section"""

    create_accordion_section(
        container,
        "💭 AI Reasoning",
        reasoning,
        icon="mi:psychology",
        color="#9c27b0",
        initially_open=False,
    )


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
        for key, value in plan_data.items():
            if key != "event_type":
                create_accordion_section(container, key, value)


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
        create_accordion_section(
            container,
            "✨ Special Touches",
            plan["special_touches"],
            icon="mi:star",
            color="#ffd700",
            initially_open=False,
        )


def add_themes_section(container, themes):
    """Render theme options with cards"""

    # Create accordion
    accordion = ColumnPanel(spacing_above="none", spacing_below="none")

    content_panel = ColumnPanel(
        visible=False,
        spacing_above="none",
        spacing_below="none",
    )

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Container",
        spacing_above="none",
        spacing_below="none",
    )

    header_btn = m3.Link(
        text=f"🎨 Theme Options ({len(themes)} options)",
        align="left",
        icon="mi:arrow_right",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        foreground="#673ab7",
    )
    header_container.add_component(header_btn)

    # Toggle
    is_expanded = {"value": False}

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

    # Add theme cards
    for i, theme in enumerate(themes, 1):
        theme_card = create_theme_card(theme, i)
        content_panel.add_component(theme_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="8px")
    card_content.add_component(content_panel)

    accordion.add_component(header_container, full_width_row=True)
    accordion.add_component(card_content)

    container.add_component(accordion)


def create_theme_card(theme, index):
    """Create a single theme card"""

    card = m3.Card(
        appearance="outlined",
        spacing_above="none",
        spacing_below="none",
    )

    card_content = m3.CardContentContainer(margin="16px")

    # Header
    header = Label(
        text=f"#{index}: {theme['name']}",
        font_size=16,
        bold=True,
        foreground="#673ab7",
    )
    card_content.add_component(header)

    # Description
    card_content.add_component(
        Label(text=theme["description"], font_size=13, spacing_above="small")
    )

    # Color palette
    if "color_palette" in theme:
        colors_panel = FlowPanel(spacing="small", spacing_above="small")
        colors_panel.add_component(
            Label(
                text="Colors:",
                bold=True,
                font_size=12,
            )
        )

        for color in theme["color_palette"]:
            # Color swatch
            color_value = (
                color
                if color.startswith("#")
                else f"#{color}"
                if len(color) == 6
                else color
            )
            color_box = Label(
                text="    ",
                background=color_value,
                border="1px solid #ccc",
            )
            colors_panel.add_component(color_box)
            colors_panel.add_component(Label(text=color, font_size=11))

        card_content.add_component(colors_panel)

    # Atmosphere
    if "atmosphere" in theme:
        atm_panel = FlowPanel(
            spacing="tiny",
            spacing_above="none",
            spacing_below="none",
        )
        atm_panel.add_component(Label(text="Atmosphere:", bold=True, font_size=12))
        atm_panel.add_component(Label(text=theme["atmosphere"], font_size=12))
        card_content.add_component(atm_panel)

    card.add_component(card_content)
    return card


def add_decorations_section(container, decorations):
    """Render decorations plan"""

    # Create accordion
    accordion = ColumnPanel(spacing_above="none", spacing_below="none")

    card = m3.Card(appearance="outlined", visible=True)  # Open by default
    content_panel = ColumnPanel(visible=True, spacing_above="none")

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Variant",
        spacing_above="small",
        spacing_below="small",
    )

    header_btn = m3.Link(
        text="🎈 Decorations",
        align="left",
        icon="mi:arrow_drop_down",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        # spacing="16px",
        foreground="#e91e63",
        background="theme:Surface Variant",
        role="filled-button",
    )
    header_container.add_component(header_btn)

    # Toggle
    is_expanded = {"value": True}

    def toggle(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        card.visible = is_expanded["value"]
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

    # Essential items
    if "essential_items" in decorations:
        content_panel.add_component(
            Label(
                text="🔴 Essential Items:",
                bold=True,
                font_size=14,
                foreground="#d32f2f",
                spacing_above="small",
            )
        )
        for item in decorations["essential_items"]:
            # bullet = FlowPanel(spacing="tiny")
            bullet = FlowPanel(
                spacing="tiny",
            )
            bullet.add_component(Label(text="  •", font_size=14, foreground="#d32f2f"))
            bullet.add_component(Label(text=item, font_size=13))
            content_panel.add_component(bullet)

    # Optional items
    if "optional_items" in decorations and decorations["optional_items"]:
        content_panel.add_component(
            Label(
                text="🔵 Optional Items:",
                bold=True,
                font_size=14,
                foreground="#1976d2",
                spacing_above="small",
            )
        )
        for item in decorations["optional_items"]:
            # bullet = FlowPanel(spacing="tiny")
            bullet = FlowPanel(spacing="tiny")
            bullet.add_component(Label(text="  •", font_size=14, foreground="#1976d2"))
            bullet.add_component(Label(text=item, font_size=13))
            content_panel.add_component(bullet)

    # DIY opportunities
    if "diy_opportunities" in decorations and decorations["diy_opportunities"]:
        content_panel.add_component(
            Label(
                text="✂️ DIY Opportunities:",
                bold=True,
                font_size=14,
                foreground="#388e3c",
                spacing_above="small",
            )
        )
        for item in decorations["diy_opportunities"]:
            # bullet = FlowPanel(spacing="tiny")
            bullet = FlowPanel(spacing="tiny")
            bullet.add_component(Label(text="  •", font_size=14, foreground="#388e3c"))
            bullet.add_component(Label(text=item, font_size=13))
            content_panel.add_component(bullet)

    # Setup tips
    if "setup_tips" in decorations:
        tip_card = m3.Card(appearance="filled", spacing_above="small")
        tip_content = m3.CardContentContainer(margin="12px")
        tip_content.add_component(Label(text="💡 Setup Tips:", bold=True, font_size=13))
        tip_content.add_component(
            Label(text=decorations["setup_tips"], font_size=12, spacing_above="tiny")
        )
        tip_card.add_component(tip_content)
        content_panel.add_component(tip_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)
    card.add_component(card_content)

    accordion.add_component(header_container, full_width_row=True)
    accordion.add_component(card)

    container.add_component(accordion)


def add_menu_options_section(container, menu_options):
    """Render menu options"""

    # Create accordion
    accordion = ColumnPanel(spacing_above="none", spacing_below="none")

    # card = m3.Card(appearance="outlined", visible=True)
    content_panel = ColumnPanel(
        visible=True,
        spacing_above="none",
        spacing_below="none",
    )

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Variant",
        spacing_above="none",
        spacing_below="none",
    )

    header_btn = m3.Link(
        text=f"🍽️ Menu Options ({len(menu_options)} options)",
        align="left",
        icon="mi:arrow_drop_down",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        # spacing="16px",
        foreground="#ff6f00",
        background="theme:Surface Variant",
        role="filled-button",
    )
    header_container.add_component(header_btn)

    # Toggle
    is_expanded = {"value": False}

    def toggle(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        # card.visible = is_expanded["value"]
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

    # Menu cards
    for i, menu in enumerate(menu_options, 1):
        menu_card = create_menu_card(menu, i)
        content_panel.add_component(menu_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px", spacing_below="none")
    card_content.add_component(content_panel)
    # card.add_component(card_content)

    accordion.add_component(header_container, full_width_row=True)
    # accordion.add_component(card)
    accordion.add_component(card_content)

    container.add_component(accordion)


def create_menu_card(menu, index):
    """Create menu option card"""

    card = m3.Card(appearance="outlined", spacing_above="small")
    card_content = m3.CardContentContainer(margin="16px")

    # Header
    card_content.add_component(
        Label(
            text=f"Option {index}: {menu['style']}",
            font_size=15,
            bold=True,
            foreground="#ff6f00",
        )
    )

    # Items
    if "items" in menu:
        card_content.add_component(
            Label(
                text="Menu Items:",
                bold=True,
                font_size=12,
                spacing_above="none",
                spacing_below="none",
            )
        )
        for item in menu["items"]:
            bullet = FlowPanel(spacing="tiny")
            bullet.add_component(Label(text="  •", font_size=12))
            bullet.add_component(Label(text=item, font_size=12))
            card_content.add_component(bullet)

    # Dietary
    if "dietary_accommodations" in menu and menu["dietary_accommodations"]:
        card_content.add_component(
            Label(text="🌱 Dietary:", bold=True, font_size=12, spacing_above="small")
        )
        for item in menu["dietary_accommodations"]:
            bullet = FlowPanel(spacing="tiny")
            bullet.add_component(Label(text="  •", font_size=12))
            bullet.add_component(Label(text=item, font_size=12))
            card_content.add_component(bullet)

    # Beverages
    if "beverage_pairings" in menu:
        card_content.add_component(
            Label(
                text="🥤 Beverages:",
                bold=True,
                font_size=12,
                spacing_above="none",
                spacing_below="none",
            )
        )
        for item in menu["beverage_pairings"]:
            bullet = FlowPanel(spacing="none")
            bullet.add_component(Label(text="  •", font_size=12))
            bullet.add_component(Label(text=item, font_size=12))
            card_content.add_component(bullet)

    card.add_component(card_content)
    return card


def add_activities_section(container, activities):
    """Render activities"""

    create_accordion_with_cards(
        container,
        f"🎮 Activities ({len(activities)} activities)",
        activities,
        create_activity_card,
        "#9c27b0",
        initially_open=True,
    )


def create_activity_card(activity, index):
    """Create activity card"""

    card = m3.Card(appearance="outlined", spacing_above="small", border="none")
    card_content = m3.CardContentContainer(margin="16px")

    # Header
    header = FlowPanel(spacing="small")
    header.add_component(
        Label(text=f"{index}. {activity['name']}", font_size=15, bold=True)
    )
    header.add_component(
        Label(text=f"⏱️ {activity['duration']}", font_size=12, foreground="#666")
    )
    card_content.add_component(header)

    # Instructions
    if "instructions" in activity:
        card_content.add_component(
            Label(
                text=activity["instructions"],
                font_size=12,
                italic=True,
                spacing_above="small",
            )
        )

    # Materials
    if "materials_needed" in activity and activity["materials_needed"]:
        card_content.add_component(
            Label(text="📦 Materials:", bold=True, font_size=12, spacing_above="small")
        )
        for material in activity["materials_needed"]:
            bullet = FlowPanel(spacing="tiny")
            bullet.add_component(Label(text="  •", font_size=12))
            bullet.add_component(Label(text=material, font_size=12))
            card_content.add_component(bullet)

    card.add_component(card_content)
    return card


def add_timeline_section(container, timeline):
    """Render timeline"""

    # Create accordion
    accordion = ColumnPanel(spacing_above="none", spacing_below="none")

    card = m3.Card(appearance="outlined", visible=True)
    content_panel = ColumnPanel(visible=True, spacing_above="none")

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Variant",
        spacing_above="none",
        spacing_below="none",
    )

    header_btn = m3.Link(
        text=f"⏰ Event Timeline ({len(timeline)} items)",
        align="left",
        icon="mi:arrow_drop_down",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        spacing="16px",
        foreground="#1976d2",
        background="theme:Surface Variant",
        role="filled-button",
    )
    header_container.add_component(header_btn)

    # Toggle
    is_expanded = {"value": True}

    def toggle(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        card.visible = is_expanded["value"]
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

    # Timeline items
    for i, item in enumerate(timeline):
        timeline_card = m3.Card(
            appearance="filled" if i % 2 == 0 else "outlined", spacing_above="small"
        )
        timeline_content = m3.CardContentContainer(margin="12px")

        # Time and activity
        time_panel = FlowPanel(spacing="small")
        time_panel.add_component(
            Label(text=item["time"], font_size=14, bold=True, foreground="#1976d2")
        )
        time_panel.add_component(Label(text=item["activity"], font_size=13))
        timeline_content.add_component(time_panel)

        # Responsible party
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
    card.add_component(card_content)

    accordion.add_component(header_container, full_width_row=True)
    accordion.add_component(card)

    container.add_component(accordion)


# ============================================================================
# PROFESSIONAL & INTELLECTUAL GATHERING (Simplified)
# ============================================================================


def add_professional_gathering_plan(container, plan):
    """Render professional gathering"""

    # Use generic accordion for all sections
    section_configs = [
        ("agenda", "📋 Agenda", "#1976d2", True),
        ("networking_approach", "🤝 Networking", "#388e3c", False),
        ("room_setup", "🏢 Room Setup", "#ff9800", False),
        ("tech_needs", "💻 Tech Requirements", "#f44336", False),
        ("refreshments", "☕ Refreshments", "#795548", False),
        ("materials", "📄 Materials", "#607d8b", False),
        ("budget_breakdown", "💰 Budget", "#4caf50", True),
    ]

    for key, title, color, open_default in section_configs:
        if key in plan:
            create_accordion_section(
                container, title, plan[key], color=color, initially_open=open_default
            )


def add_intellectual_gathering_plan(container, plan):
    """Render intellectual gathering"""

    section_configs = [
        ("discussion_format", "💬 Discussion Format", "#7b1fa2", True),
        ("preparation_guidelines", "📚 Preparation", "#5e35b1", False),
        ("discussion_prompts", "💡 Discussion Prompts", "#7b1fa2", True),
        ("seating_arrangement", "🪑 Seating", "#388e3c", False),
        ("refreshments", "☕ Refreshments", "#795548", False),
        ("materials_needed", "📖 Materials", "#e64a19", False),
        ("budget_breakdown", "💰 Budget", "#4caf50", True),
    ]

    for key, title, color, open_default in section_configs:
        if key in plan:
            create_accordion_section(
                container, title, plan[key], color=color, initially_open=open_default
            )


# ============================================================================
# BUDGET SECTION
# ============================================================================


def add_budget_breakdown_section(container, budget_items):
    """Render budget with visual bars"""

    # Create accordion
    accordion = ColumnPanel(spacing_above="none", spacing_below="none")

    card = m3.Card(appearance="outlined", visible=True)
    content_panel = ColumnPanel(visible=True, spacing_above="none")

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Variant",
        spacing_above="none",
        spacing_below="none",
    )

    header_btn = m3.Link(
        text=f"💰 Budget Breakdown ({len(budget_items)} categories)",
        align="left",
        icon="mi:arrow_drop_down",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        spacing="16px",
        foreground="#4caf50",
        background="theme:Surface Variant",
        role="filled-button",
    )
    header_container.add_component(header_btn)

    # Toggle
    is_expanded = {"value": True}

    def toggle(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        card.visible = is_expanded["value"]
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

    # Total
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

    # Budget items
    for item in budget_items:
        budget_card = create_budget_card(item)
        content_panel.add_component(budget_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)
    card.add_component(card_content)

    accordion.add_component(header_container, full_width_row=True)
    accordion.add_component(card)

    container.add_component(accordion)


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

    # Progress bar (visual representation)
    bar_container = ColumnPanel(
        background="#e0e0e0",
        spacing_above="small",
    )
    bar_fill = Label(
        text="  ",
        background="#4caf50",
    )
    # Width based on percentage (capped at 100%)
    bar_width = min(int(percentage), 100)
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
# HELPER FUNCTIONS
# ============================================================================


def create_accordion_with_cards(
    container, title, items, card_creator, color="#2196f3", initially_open=True
):
    """Generic accordion with item cards"""

    accordion = ColumnPanel(spacing_above="none", spacing_below="none")

    card = m3.Card(appearance="outlined", visible=initially_open)
    content_panel = ColumnPanel(visible=initially_open, spacing_above="none")

    # Header
    header_container = ColumnPanel(
        background="theme:Surface Variant"
        if initially_open
        else "theme:Surface Container",
        spacing_above="none",
        spacing_below="none",
    )

    header_btn = m3.Link(
        text=title,
        align="left",
        icon="mi:arrow_drop_down" if initially_open else "mi:arrow_right",
        icon_size="16px",
        icon_align="left",
        underline=False,
        bold=True,
        spacing="16px",
        foreground=color,
    )

    if initially_open:
        header_btn.background = "theme:Surface Variant"
        header_btn.role = "filled-button"

    header_container.add_component(header_btn)

    # Toggle
    is_expanded = {"value": initially_open}

    def toggle(**event_args):
        is_expanded["value"] = not is_expanded["value"]
        content_panel.visible = is_expanded["value"]
        card.visible = is_expanded["value"]
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

    # Add items
    for i, item in enumerate(items, 1):
        item_card = card_creator(item, i)
        content_panel.add_component(item_card)

    # Assemble
    card_content = m3.CardContentContainer(margin="16px")
    card_content.add_component(content_panel)
    card.add_component(card_content)

    accordion.add_component(header_container, full_width_row=True)
    accordion.add_component(card)

    container.add_component(accordion)


def create_item_card(item):
    """Generic item card from dict"""

    card = m3.Card(appearance="outlined", spacing_above="small")
    card_content = m3.CardContentContainer(margin="12px")

    for key, value in item.items():
        if isinstance(value, list):
            card_content.add_component(
                Label(text=f"{format_title(key)}:", bold=True, font_size=12)
            )
            for v in value:
                bullet = FlowPanel(spacing="tiny")
                bullet.add_component(Label(text="    •", font_size=12))
                bullet.add_component(Label(text=str(v), font_size=12))
                card_content.add_component(bullet)
        else:
            row = create_key_value_row(key, value)
            card_content.add_component(row)

    card.add_component(card_content)
    return card


def create_key_value_row(key, value):
    """Create key-value row"""

    row = FlowPanel(spacing="tiny", spacing_above="tiny")
    row.add_component(Label(text=f"{format_title(key)}:", bold=True, font_size=12))
    row.add_component(Label(text=str(value), font_size=12))
    return row


def format_title(text):
    """Format key to title"""
    return text.replace("_", " ").title()

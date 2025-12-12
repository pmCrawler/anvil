# ClientModules/ai_ui_builder.py

"""
Dynamic UI Builder for AI Responses
Automatically generates Anvil UI components from structured data
"""

from anvil import *
import anvil.server

# ============================================================================
# MAIN UI BUILDER
# ============================================================================


def build_ai_response_ui(response_data, container):
    """
    Build dynamic UI from AI response data

    Args:
        response_data (dict): The AI response data
        container: Anvil container to add components to (ColumnPanel, etc.)
    """

    # Clear existing content
    container.clear()

    # Check for metadata
    meta = response_data.get("_meta", {})
    response_type = meta.get("type", "unknown")

    # Add header with metadata
    if meta:
        add_metadata_header(container, meta)

    # Build UI based on data structure
    for key, value in response_data.items():
        if key == "_meta":
            continue  # Skip metadata, already handled

        # Create section for each root element
        add_section(container, key, value)

    # Add action buttons at bottom
    add_action_buttons(container, response_data)


# ============================================================================
# SECTION BUILDERS
# ============================================================================


def add_section(container, key, value):
    """Add a section with appropriate component based on value type"""

    # Skip if None
    if value is None:
        return

    # Determine component type based on value
    if isinstance(value, list):
        add_list_section(container, key, value)
    elif isinstance(value, dict):
        add_object_section(container, key, value)
    elif isinstance(value, (int, float)):
        add_numeric_section(container, key, value)
    elif isinstance(value, bool):
        add_boolean_section(container, key, value)
    else:  # String
        add_text_section(container, key, value)


def add_list_section(container, key, items):
    """Handle list/array data - use accordion with cards or data grid"""

    # Create expandable section
    expander = create_expander(title=format_title(key), badge=f"{len(items)} items")

    # Check if items are objects/dicts (use cards) or simple values (use bullets)
    if items and isinstance(items[0], dict):
        # Complex objects - render as cards
        for i, item in enumerate(items):
            card = create_card_from_dict(item, index=i + 1)
            expander.content.add_component(card)
    else:
        # Simple list - render as bullet points
        bullet_panel = create_bullet_list(items)
        expander.content.add_component(bullet_panel)

    container.add_component(expander)


def add_object_section(container, key, obj):
    """Handle nested object/dict"""

    expander = create_expander(title=format_title(key))

    # Recursively build content for nested object
    for sub_key, sub_value in obj.items():
        add_section(expander.content, sub_key, sub_value)

    container.add_component(expander)


def add_text_section(container, key, text):
    """Handle text values"""

    # Short text - inline
    if len(str(text)) < 100:
        row = LinearPanel(spacing="small")
        row.add_component(Label(text=f"{format_title(key)}:", font_size=14, bold=True))
        row.add_component(Label(text=str(text), font_size=14))
        container.add_component(row)
    else:
        # Long text - expandable
        expander = create_expander(title=format_title(key))
        expander.content.add_component(Label(text=str(text), font_size=14))
        container.add_component(expander)


def add_numeric_section(container, key, value):
    """Handle numeric values with formatting"""

    row = LinearPanel(spacing="small")
    row.add_component(Label(text=f"{format_title(key)}:", font_size=14, bold=True))

    # Format based on key name
    if "price" in key.lower() or "budget" in key.lower() or "amount" in key.lower():
        formatted = f"${value:,.2f}"
    elif "percentage" in key.lower() or "percent" in key.lower():
        formatted = f"{value:.1f}%"
    elif "rating" in key.lower():
        formatted = f"⭐ {value:.1f}/5.0"
    else:
        formatted = f"{value:,.0f}" if isinstance(value, int) else f"{value:.2f}"

    row.add_component(
        Label(text=formatted, font_size=16, bold=True, foreground="#2196F3")
    )

    container.add_component(row)


def add_boolean_section(container, key, value):
    """Handle boolean values"""

    row = LinearPanel(spacing="small")
    icon = "✅" if value else "❌"
    row.add_component(Label(text=f"{icon} {format_title(key)}", font_size=14))
    container.add_component(row)


# ============================================================================
# COMPONENT CREATORS
# ============================================================================


def create_expander(title, badge=None):
    """Create collapsible expander/accordion section"""

    # Container for expander
    expander_container = ColumnPanel(spacing="small")

    # Header (clickable)
    header = LinearPanel(
        background="#f5f5f5",
        spacing="small",
        spacing_above="small",
        spacing_below="none",
    )

    # Title
    title_label = Label(
        text=f"▶ {title}", font_size=16, bold=True, icon="fa:chevron-right"
    )
    header.add_component(title_label)

    # Badge (if provided)
    if badge:
        badge_label = Label(
            text=badge,
            font_size=12,
            background="#2196F3",
            foreground="white",
            spacing="small",
        )
        header.add_component(badge_label)

    # Content (initially hidden)
    content = ColumnPanel(visible=False, spacing="small", background="#fafafa")

    # Toggle function
    def toggle_expand(**event_args):
        content.visible = not content.visible
        if content.visible:
            title_label.text = f"▼ {title}"
            title_label.icon = "fa:chevron-down"
        else:
            title_label.text = f"▶ {title}"
            title_label.icon = "fa:chevron-right"

    header.set_event_handler("click", toggle_expand)

    # Assemble
    expander_container.add_component(header)
    expander_container.add_component(content)

    # Add content property for easy access
    expander_container.content = content

    return expander_container


def create_card_from_dict(data, index=None):
    """Create a styled card from dictionary data"""

    card = ColumnPanel(
        background="white",
        border="1px solid #e0e0e0",
        spacing="small",
        spacing_above="small",
        spacing_below="small",
    )

    # Card header (if has name/title)
    title_key = next(
        (k for k in ["name", "title", "task", "category"] if k in data), None
    )
    if title_key:
        header = Label(
            text=f"#{index}: {data[title_key]}" if index else data[title_key],
            font_size=16,
            bold=True,
            foreground="#1976D2",
        )
        card.add_component(header)

    # Card content
    for key, value in data.items():
        if key == title_key:
            continue  # Already used in header

        if isinstance(value, list):
            # Nested list - show as bullets
            label = Label(text=f"{format_title(key)}:", font_size=13, bold=True)
            card.add_component(label)

            bullets = create_bullet_list(value)
            card.add_component(bullets)

        elif isinstance(value, dict):
            # Nested object
            label = Label(text=f"{format_title(key)}:", font_size=13, bold=True)
            card.add_component(label)

            nested_card = create_card_from_dict(value)
            card.add_component(nested_card)

        else:
            # Simple value
            row = LinearPanel(spacing="tiny")
            row.add_component(
                Label(text=f"{format_title(key)}:", font_size=13, bold=True)
            )
            row.add_component(Label(text=format_value(key, value), font_size=13))
            card.add_component(row)

    return card


def create_bullet_list(items):
    """Create bullet point list"""

    panel = ColumnPanel(spacing="tiny")

    for item in items:
        bullet = LinearPanel(spacing="tiny")
        bullet.add_component(Label(text="•", font_size=14))
        bullet.add_component(Label(text=str(item), font_size=13))
        panel.add_component(bullet)

    return panel


def create_data_grid(data_list, columns=None):
    """Create data grid for tabular data"""

    if not data_list or not isinstance(data_list[0], dict):
        return Label(text="[Invalid data for grid]")

    # Auto-detect columns if not provided
    if columns is None:
        columns = list(data_list[0].keys())

    # Create DataGrid
    grid = DataGrid(
        auto_header=True,
        columns=[
            {"id": col, "title": format_title(col), "data_key": col} for col in columns
        ],
    )

    grid.items = data_list

    return grid


# ============================================================================
# UTILITIES
# ============================================================================


def format_title(text):
    """Convert snake_case to Title Case"""
    return text.replace("_", " ").title()


def format_value(key, value):
    """Format value based on key name"""

    if value is None:
        return "N/A"

    key_lower = key.lower()

    # Money
    if any(word in key_lower for word in ["price", "budget", "amount", "cost"]):
        try:
            return f"${float(value):,.2f}"
        except:
            return str(value)

    # Percentage
    if "percent" in key_lower or "percentage" in key_lower:
        try:
            return f"{float(value):.1f}%"
        except:
            return str(value)

    # Rating
    if "rating" in key_lower:
        try:
            return f"⭐ {float(value):.1f}/5.0"
        except:
            return str(value)

    # Capacity/count
    if any(word in key_lower for word in ["capacity", "count", "number"]):
        try:
            return f"{int(value):,}"
        except:
            return str(value)

    return str(value)


def add_metadata_header(container, meta):
    """Add metadata header with timestamp and model info"""

    header = LinearPanel(
        background="#e3f2fd",
        spacing="small",
        spacing_above="none",
        spacing_below="small",
    )

    header.add_component(Label(text="🤖 AI Generated", font_size=12, bold=True))

    if meta.get("model"):
        header.add_component(Label(text=f"Model: {meta['model']}", font_size=11))

    if meta.get("timestamp"):
        header.add_component(
            Label(text=f"Generated: {meta['timestamp'][:19]}", font_size=11)
        )

    container.add_component(header)


def add_action_buttons(container, response_data):
    """Add action buttons at bottom"""

    button_panel = LinearPanel(spacing="small", spacing_above="medium")

    # Save button
    save_btn = Button(text="💾 Save Response", icon="fa:save", role="primary-color")
    save_btn.response_data = response_data  # Store data
    button_panel.add_component(save_btn)

    # Export button
    export_btn = Button(text="📤 Export", icon="fa:download")
    export_btn.response_data = response_data
    button_panel.add_component(export_btn)

    # Share button
    share_btn = Button(text="🔗 Share", icon="fa:share-alt")
    button_panel.add_component(share_btn)

    container.add_component(button_panel)


# ============================================================================
# SPECIALIZED BUILDERS (Optional)
# ============================================================================


def build_venue_suggestions_ui(data, container):
    """Specialized builder for venue suggestions"""

    container.clear()

    # Summary at top
    if "summary" in data:
        summary_card = ColumnPanel(
            background="#e8f5e9",
            spacing="small",
            spacing_above="none",
            spacing_below="small",
        )
        summary_card.add_component(Label(text="📋 Summary", font_size=16, bold=True))
        summary_card.add_component(Label(text=data["summary"], font_size=14))
        container.add_component(summary_card)

    # Venue suggestions
    if "suggestions" in data:
        add_list_section(container, "suggestions", data["suggestions"])

    # Tips
    if "tips" in data:
        add_list_section(container, "tips", data["tips"])


def build_budget_plan_ui(data, container):
    """Specialized builder for budget plan"""

    container.clear()

    # Total budget highlight
    if "total_budget" in data:
        total_card = ColumnPanel(background="#fff3e0", spacing="small")
        total_card.add_component(Label(text="💰 Total Budget", font_size=16, bold=True))
        total_card.add_component(
            Label(
                text=f"${data['total_budget']:,.2f}",
                font_size=24,
                bold=True,
                foreground="#ff6f00",
            )
        )
        container.add_component(total_card)

    # Budget breakdown
    if "breakdown" in data:
        add_list_section(container, "breakdown", data["breakdown"])

    # Contingency and warnings
    for key in ["contingency", "summary", "warnings"]:
        if key in data:
            add_section(container, key, data[key])


def build_task_checklist_ui(data, container):
    """Specialized builder for task checklist"""

    container.clear()

    # Timeline
    if "timeline" in data:
        add_text_section(container, "timeline", data["timeline"])

    # Tasks with priority indicators
    if "tasks" in data:
        tasks_expander = create_expander(
            title="📝 Tasks", badge=f"{len(data['tasks'])} tasks"
        )

        for i, task in enumerate(data["tasks"]):
            task_card = create_task_card(task, index=i + 1)
            tasks_expander.content.add_component(task_card)

        container.add_component(tasks_expander)

    # Milestones and tips
    for key in ["milestones", "tips"]:
        if key in data:
            add_section(container, key, data[key])


def create_task_card(task, index):
    """Create styled task card with priority indicator"""

    # Color based on priority
    priority_colors = {"high": "#f44336", "medium": "#ff9800", "low": "#4caf50"}

    priority = task.get("priority", "medium").lower()
    border_color = priority_colors.get(priority, "#9e9e9e")

    card = ColumnPanel(
        background="white",
        border=f"3px solid {border_color}",
        spacing="small",
        spacing_above="small",
    )

    # Header with priority badge
    header = LinearPanel(spacing="small")
    header.add_component(
        Label(text=f"#{index}", font_size=12, background="#f5f5f5", foreground="#666")
    )
    header.add_component(
        Label(text=task.get("task", "Untitled"), font_size=15, bold=True)
    )
    header.add_component(
        Label(
            text=priority.upper(),
            font_size=11,
            background=border_color,
            foreground="white",
            bold=True,
        )
    )
    card.add_component(header)

    # Details
    for key in ["deadline", "estimated_time", "notes"]:
        if key in task and task[key]:
            row = LinearPanel(spacing="tiny")
            row.add_component(
                Label(text=f"{format_title(key)}:", font_size=12, bold=True)
            )
            row.add_component(Label(text=task[key], font_size=12))
            card.add_component(row)

    return card

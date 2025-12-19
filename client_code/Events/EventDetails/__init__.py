# Events/EventView/__init__.py

from ._anvil_designer import EventDetailsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.users
import m3.components as m3
from anvil.tables import app_tables


class EventDetails(EventDetailsTemplate):
    def __init__(self, event_id=24, **properties):
        self.init_components(**properties)

        self.event_id = event_id
        self.event_data = None

        if event_id:
            self.load_event_data()
        else:
            alert("No event ID provided", title="Error")
            open_form("Events")

    def load_event_data(self):
        """Load event data from server"""
        with Notification("Loading event...", timeout=None):
            try:
                result = anvil.server.call("get_event_details", self.event_id)

                if result["success"]:
                    self.event_data = result["event"]
                    self.render_event_view()
                else:
                    alert(f"Error loading event: {result.get('error')}", title="Error")
                    open_form("Events")
            except Exception as e:
                print(f"Error loading event: {e}")
                alert(f"Failed to load event: {str(e)}", title="Error")
                open_form("Events")

    def render_event_view(self):
        """Render the complete event view"""

        # Clear container
        self.column_panel_main.clear()

        # Header Section
        self.add_event_header()

        # Quick Stats Row
        self.add_quick_stats()

        # Main Content Grid (2 columns)
        content_grid = FlowPanel(spacing="medium", align="left")

        # Left Column (60% width)
        left_column = ColumnPanel(spacing="medium")

        # Event Details Card
        self.add_event_details_card(left_column)

        # Selected Options Card
        if self.event_data.get("event_options"):
            self.add_selected_options_card(left_column)

        # AI Plan Sections (decorations, logistics, etc.)
        if self.event_data.get("ai_response"):
            self.add_ai_plan_sections(left_column)

        content_grid.add_component(left_column, width="60%")

        # Right Column (40% width)
        right_column = ColumnPanel(spacing="medium")

        # Tasks Card
        self.add_tasks_card(right_column)

        # Budget Card
        self.add_budget_card(right_column)

        # Timeline Card
        self.add_timeline_card(right_column)

        content_grid.add_component(right_column, width="40%")

        self.column_panel_main.add_component(content_grid)

        # Action Buttons
        self.add_action_buttons()

    # ========================================================================
    # HEADER SECTION
    # ========================================================================

    def add_event_header(self):
        """Add event header with title and status"""

        header = ColumnPanel(
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            spacing="medium",
        )

        # Title row
        title_row = FlowPanel(spacing="medium", align="left")

        title_row.add_component(
            Label(
                text=self.event_data["title"],
                font_size=28,
                bold=True,
                # foreground="white"
            )
        )

        # Status badge
        status = self.event_data.get("status", "planning")
        status_colors = {
            "planning": "#ff9800",
            "confirmed": "#4caf50",
            "completed": "#2196f3",
            "cancelled": "#f44336",
        }

        status_badge = Label(
            text=status.upper(),
            font_size=12,
            bold=True,
            background=status_colors.get(status, "#757575"),
            # foreground="white"
            spacing="small",
        )
        title_row.add_component(status_badge)

        header.add_component(title_row)

        # Description
        if self.event_data.get("description"):
            header.add_component(
                Label(
                    text=self.event_data["description"],
                    font_size=15,
                    # foreground="white"
                    italic=True,
                )
            )

        # Date & Location row
        info_row = FlowPanel(spacing="large", align="left")

        # Date
        event_date = self.event_data.get("event_datetime")
        if event_date:
            date_panel = FlowPanel(spacing="tiny")
            date_panel.add_component(Label(text="📅", font_size=18))
            date_panel.add_component(
                Label(
                    text=event_date.strftime("%B %d, %Y at %I:%M %p")
                    if hasattr(event_date, "strftime")
                    else str(event_date),
                    font_size=14,
                    # foreground="white"
                    bold=True,
                )
            )
            info_row.add_component(date_panel)

        # Location
        location = self.event_data.get("location")
        if location and location.get("formatted_address"):
            loc_panel = FlowPanel(spacing="tiny")
            loc_panel.add_component(Label(text="📍", font_size=18))
            loc_panel.add_component(
                Label(
                    text=location["formatted_address"], font_size=14, foreground="white"
                )
            )
            info_row.add_component(loc_panel)

        header.add_component(info_row)

        self.column_panel_main.add_component(header)

    # ========================================================================
    # QUICK STATS
    # ========================================================================

    def add_quick_stats(self):
        """Add quick stats cards"""

        stats_panel = FlowPanel(
            spacing="medium",
            align="left",
            spacing_above="medium",
        )

        # Guest Count
        stats_panel.add_component(
            self.create_stat_card(
                icon="👥",
                value=str(self.event_data.get("guest_count", 0)),
                label="Guests",
                color="#2196f3",
            )
        )

        # Budget
        budget = self.event_data.get("budget", 0)
        stats_panel.add_component(
            self.create_stat_card(
                icon="💰",
                value=f"${budget:,.0f}" if budget else "$0",
                label="Budget",
                color="#4caf50",
            )
        )

        # Tasks
        tasks = self.event_data.get("tasks", [])
        completed_tasks = sum(1 for t in tasks if t.get("is_done"))
        stats_panel.add_component(
            self.create_stat_card(
                icon="✓",
                value=f"{completed_tasks}/{len(tasks)}",
                label="Tasks Done",
                color="#ff9800",
            )
        )

        # Days Until
        event_date = self.event_data.get("event_datetime")
        if event_date:
            from datetime import datetime, timezone

            if isinstance(event_date, str):
                event_date = datetime.fromisoformat(event_date.replace("Z", "+00:00"))

            days_until = (event_date - datetime.now(timezone.utc)).days

            if days_until < 0:
                days_text = "Past"
                color = "#757575"
            elif days_until == 0:
                days_text = "Today!"
                color = "#f44336"
            elif days_until == 1:
                days_text = "Tomorrow"
                color = "#ff5722"
            else:
                days_text = f"{days_until} days"
                color = "#9c27b0"

            stats_panel.add_component(
                self.create_stat_card(
                    icon="📆",
                    value=days_text,
                    label="Until Event",
                    color=color,
                )
            )

        self.column_panel_main.add_component(stats_panel)

    def create_stat_card(self, icon, value, label, color):
        """Create a stat card"""

        card = m3.Card(appearance="elevated")
        card_content = m3.CardContentContainer(margin="16px")

        # Icon
        card_content.add_component(Label(text=icon, font_size=32, align="center"))

        # Value
        card_content.add_component(
            Label(text=value, font_size=24, bold=True, align="center", foreground=color)
        )

        # Label
        card_content.add_component(
            Label(text=label, font_size=12, align="center", foreground="#666")
        )

        card.add_component(card_content)
        return card

    # ========================================================================
    # EVENT DETAILS CARD
    # ========================================================================

    def add_event_details_card(self, container):
        """Add editable event details card"""

        card = m3.Card(appearance="outlined")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        header = FlowPanel(spacing="medium", align="left")
        header.add_component(
            Label(
                text="📋 Event Details", font_size=20, bold=True, foreground="#1976d2"
            )
        )

        # Edit button
        edit_btn = m3.Button(
            text="Edit", icon="mi:edit", appearance="outlined", size="small"
        )
        edit_btn.set_event_handler("click", self.edit_event_details)
        header.add_component(edit_btn)

        card_content.add_component(header)

        # Details grid
        details_grid = ColumnPanel(spacing="small", spacing_above="medium")

        # Venue Type
        details_grid.add_component(
            self.create_detail_row(
                "🏢 Venue Type:", self.event_data.get("venue_type", "Not specified")
            )
        )

        # Event Setting
        details_grid.add_component(
            self.create_detail_row(
                "🎭 Setting:", self.event_data.get("event_setting", "Not specified")
            )
        )

        # Food & Beverage
        details_grid.add_component(
            self.create_detail_row(
                "🍽️ Food & Beverage:", "Yes" if self.event_data.get("food_bev") else "No"
            )
        )

        # Created
        created_at = self.event_data.get("created_at")
        if created_at:
            details_grid.add_component(
                self.create_detail_row(
                    "📅 Created:",
                    created_at.strftime("%B %d, %Y")
                    if hasattr(created_at, "strftime")
                    else str(created_at),
                )
            )

        card_content.add_component(details_grid)
        card.add_component(card_content)
        container.add_component(card)

    def create_detail_row(self, label, value):
        """Create a detail row"""
        row = FlowPanel(spacing="small", align="left")
        row.add_component(Label(text=label, bold=True, font_size=13, foreground="#666"))
        row.add_component(Label(text=str(value), font_size=13))
        return row

    # ========================================================================
    # SELECTED OPTIONS CARD
    # ========================================================================

    def add_selected_options_card(self, container):
        """Add selected options from AI"""

        card = m3.Card(appearance="filled", spacing_above="medium")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        card_content.add_component(
            Label(
                text="⭐ Your Selected Options",
                font_size=20,
                bold=True,
                foreground="#7b1fa2",
            )
        )

        options = self.event_data["event_options"]

        # Render each selected option
        for section_key, selection in options.items():
            section_title = section_key.replace("_", " ").title()

            # Section header
            card_content.add_component(
                Label(
                    text=f"• {section_title}",
                    font_size=15,
                    bold=True,
                    spacing_above="medium",
                    foreground="#9c27b0",
                )
            )

            # Selection content
            if isinstance(selection, dict):
                # Single selection - show as card
                option_card = self.create_option_display_card(selection)
                card_content.add_component(option_card)
            elif isinstance(selection, list):
                # Multiple selections
                for item in selection:
                    option_card = self.create_option_display_card(item)
                    card_content.add_component(option_card)

        card.add_component(card_content)
        container.add_component(card)

    def create_option_display_card(self, option):
        """Create display card for selected option"""

        card = m3.Card(appearance="outlined", spacing_above="small")
        card_content = m3.CardContentContainer(margin="12px")

        # Show key fields
        for key, value in option.items():
            if key in ["name", "style", "title"]:
                # Main title
                card_content.add_component(
                    Label(text=value, font_size=14, bold=True, foreground="#673ab7")
                )
            elif key == "description":
                # Description
                card_content.add_component(
                    Label(text=value, font_size=12, spacing_above="tiny")
                )
            elif isinstance(value, list) and len(value) < 5:
                # Short lists
                card_content.add_component(
                    Label(
                        text=f"{key.replace('_', ' ').title()}: {', '.join(str(v) for v in value)}",
                        font_size=11,
                        foreground="#666",
                        spacing_above="tiny",
                    )
                )

        card.add_component(card_content)
        return card

    # ========================================================================
    # AI PLAN SECTIONS (Decorations, Logistics, etc.)
    # ========================================================================

    def add_ai_plan_sections(self, container):
        """Add non-selectable AI plan sections"""

        ai_response = self.event_data.get("ai_response", {})
        plan = ai_response.get("plan", {})

        # Decorations
        if "decorations" in plan:
            self.add_decorations_section(container, plan["decorations"])

        # Logistics
        if "logistics" in ai_response:
            self.add_simple_section(container, "🚚 Logistics", ai_response["logistics"])

        # Contingency Plans
        if "contingency_notes" in ai_response:
            self.add_simple_section(
                container, "🛡️ Contingency Plans", ai_response["contingency_notes"]
            )

    def add_decorations_section(self, container, decorations):
        """Add decorations section"""

        card = m3.Card(appearance="outlined", spacing_above="medium")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        card_content.add_component(
            Label(text="🎈 Decorations", font_size=18, bold=True, foreground="#e91e63")
        )

        # Essential items
        if "essential_items" in decorations:
            card_content.add_component(
                Label(
                    text="Essential Items:",
                    bold=True,
                    font_size=14,
                    spacing_above="medium",
                    foreground="#d32f2f",
                )
            )
            for item in decorations["essential_items"]:
                card_content.add_component(self.create_bullet_item(item, "🔴"))

        # Optional items
        if "optional_items" in decorations and decorations["optional_items"]:
            card_content.add_component(
                Label(
                    text="Optional Items:",
                    bold=True,
                    font_size=14,
                    spacing_above="small",
                    foreground="#1976d2",
                )
            )
            for item in decorations["optional_items"]:
                card_content.add_component(self.create_bullet_item(item, "🔵"))

        # Setup tips
        if "setup_tips" in decorations:
            tip_card = m3.Card(appearance="filled", spacing_above="small")
            tip_content = m3.CardContentContainer(margin="12px")
            tip_content.add_component(
                Label(text="💡 Setup Tips:", bold=True, font_size=13)
            )
            tip_content.add_component(
                Label(text=decorations["setup_tips"], font_size=12)
            )
            tip_card.add_component(tip_content)
            card_content.add_component(tip_card)

        card.add_component(card_content)
        container.add_component(card)

    def add_simple_section(self, container, title, items):
        """Add simple list section"""

        card = m3.Card(appearance="outlined", spacing_above="medium")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        card_content.add_component(
            Label(text=title, font_size=18, bold=True, foreground="#3f51b5")
        )

        # Items
        if isinstance(items, list):
            for item in items:
                card_content.add_component(self.create_bullet_item(item))
        else:
            card_content.add_component(Label(text=str(items), font_size=13))

        card.add_component(card_content)
        container.add_component(card)

    def create_bullet_item(self, text, icon="•"):
        """Create bullet item"""
        row = FlowPanel(spacing="tiny", spacing_above="tiny")
        row.add_component(Label(text=icon, font_size=14))
        row.add_component(Label(text=str(text), font_size=13))
        return row

    # ========================================================================
    # TASKS CARD
    # ========================================================================

    def add_tasks_card(self, container):
        """Add tasks management card"""

        card = m3.Card(appearance="outlined")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        header = FlowPanel(spacing="medium", align="left")
        header.add_component(
            Label(text="✓ Tasks", font_size=18, bold=True, foreground="#ff9800")
        )

        # Add task button
        add_btn = m3.Button(
            text="Add", icon="mi:add", appearance="outlined", size="small"
        )
        add_btn.set_event_handler("click", self.add_new_task)
        header.add_component(add_btn)

        card_content.add_component(header)

        # Tasks list
        tasks = self.event_data.get("tasks", [])

        if not tasks:
            card_content.add_component(
                Label(
                    text="No tasks yet. Click Add to create one.",
                    font_size=13,
                    italic=True,
                    foreground="#999",
                    spacing_above="medium",
                )
            )
        else:
            for task in tasks:
                task_card = self.create_task_card(task)
                card_content.add_component(task_card)

        card.add_component(card_content)
        container.add_component(card)

    def create_task_card(self, task):
        """Create individual task card"""

        task_card = m3.Card(
            appearance="filled" if not task.get("is_done") else "outlined",
            spacing_above="small",
        )
        task_content = m3.CardContentContainer(margin="12px")

        # Task row
        task_row = FlowPanel(spacing="small", align="left")

        # Checkbox
        checkbox = CheckBox(checked=task.get("is_done", False), font_size=14)
        checkbox.tag.task_id = task["id"]
        checkbox.set_event_handler("change", self.toggle_task_complete)
        task_row.add_component(checkbox)

        # Task text
        task_text = Label(
            text=task["task"],
            font_size=14,
            bold=not task.get("is_done"),
            foreground="#999" if task.get("is_done") else "#000",
        )
        if task.get("is_done"):
            task_text.text = f"~~{task_text.text}~~"  # Strikethrough
        task_row.add_component(task_text)

        task_content.add_component(task_row)

        # Due date
        if task.get("due_date"):
            due_date = task["due_date"]
            task_content.add_component(
                Label(
                    text=f"📅 Due: {due_date.strftime('%b %d') if hasattr(due_date, 'strftime') else str(due_date)}",
                    font_size=11,
                    foreground="#666",
                    spacing_above="tiny",
                )
            )

        # Details
        if task.get("details"):
            task_content.add_component(
                Label(
                    text=task["details"],
                    font_size=11,
                    foreground="#666",
                    spacing_above="tiny",
                )
            )

        task_card.add_component(task_content)
        return task_card

    # ========================================================================
    # BUDGET CARD
    # ========================================================================

    def add_budget_card(self, container):
        """Add budget tracking card"""

        card = m3.Card(appearance="outlined", spacing_above="medium")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        header = FlowPanel(spacing="medium", align="left")
        header.add_component(
            Label(text="💰 Budget", font_size=18, bold=True, foreground="#4caf50")
        )

        # Add item button
        add_btn = m3.Button(
            text="Add", icon="mi:add", appearance="outlined", size="small"
        )
        add_btn.set_event_handler("click", self.add_budget_item)
        header.add_component(add_btn)

        card_content.add_component(header)

        # Total budget
        budget = self.event_data.get("budget", 0)
        budget_items = self.event_data.get("budget_items", [])

        # Calculate totals
        estimated_total = sum(item.get("estimated_amount", 0) for item in budget_items)
        actual_total = sum(item.get("actual_amount", 0) for item in budget_items)

        # Total card
        total_card = m3.Card(appearance="filled", spacing_above="small")
        total_content = m3.CardContentContainer(margin="12px")

        total_content.add_component(
            Label(
                text=f"Total Budget: ${budget:,.2f}",
                font_size=16,
                bold=True,
                foreground="#2e7d32",
            )
        )

        if budget_items:
            total_content.add_component(
                Label(
                    text=f"Estimated: ${estimated_total:,.2f} | Actual: ${actual_total:,.2f}",
                    font_size=12,
                    foreground="#666",
                )
            )

            # Progress bar
            if budget > 0:
                percentage = min((estimated_total / budget) * 100, 100)
                color = "#4caf50" if percentage <= 100 else "#f44336"

                total_content.add_component(
                    Label(
                        text=f"{percentage:.0f}% allocated",
                        font_size=11,
                        foreground=color,
                        spacing_above="tiny",
                    )
                )

        total_card.add_component(total_content)
        card_content.add_component(total_card)

        # Budget items
        if not budget_items:
            card_content.add_component(
                Label(
                    text="No budget items yet.",
                    font_size=13,
                    italic=True,
                    foreground="#999",
                    spacing_above="medium",
                )
            )
        else:
            for item in budget_items:
                budget_item_card = self.create_budget_item_card(item)
                card_content.add_component(budget_item_card)

        card.add_component(card_content)
        container.add_component(card)

    def create_budget_item_card(self, item):
        """Create budget item card"""

        item_card = m3.Card(appearance="outlined", spacing_above="small")
        item_content = m3.CardContentContainer(margin="12px")

        # Header
        header = FlowPanel(spacing="small", align="left")
        header.add_component(Label(text=item["category"], font_size=13, bold=True))

        # Paid badge
        if item.get("paid"):
            header.add_component(
                Label(
                    text="PAID",
                    font_size=10,
                    bold=True,
                    background="#4caf50",
                    # foreground="white"
                )
            )

        item_content.add_component(header)

        # Amounts
        estimated = item.get("estimated_amount", 0)
        actual = item.get("actual_amount", 0)

        item_content.add_component(
            Label(
                text=f"Estimated: ${estimated:,.2f}"
                + (f" | Actual: ${actual:,.2f}" if actual else ""),
                font_size=11,
                foreground="#666",
            )
        )

        # Description
        if item.get("description"):
            item_content.add_component(
                Label(
                    text=item["description"],
                    font_size=11,
                    foreground="#999",
                    italic=True,
                    spacing_above="tiny",
                )
            )

        item_card.add_component(item_content)
        return item_card

    # ========================================================================
    # TIMELINE CARD
    # ========================================================================

    def add_timeline_card(self, container):
        """Add event timeline card"""

        card = m3.Card(appearance="outlined", spacing_above="medium")
        card_content = m3.CardContentContainer(margin="16px")

        # Header
        card_content.add_component(
            Label(text="⏰ Timeline", font_size=18, bold=True, foreground="#1976d2")
        )

        # Get timeline from AI response
        ai_response = self.event_data.get("ai_response", {})
        timeline = ai_response.get("plan", {}).get("timeline", [])

        if not timeline:
            card_content.add_component(
                Label(
                    text="No timeline available.",
                    font_size=13,
                    italic=True,
                    foreground="#999",
                    spacing_above="medium",
                )
            )
        else:
            for i, item in enumerate(timeline):
                timeline_item = self.create_timeline_item(item, i)
                card_content.add_component(timeline_item)

        card.add_component(card_content)
        container.add_component(card)

    def create_timeline_item(self, item, index):
        """Create timeline item"""

        item_card = m3.Card(
            appearance="filled" if index % 2 == 0 else "outlined", spacing_above="small"
        )
        item_content = m3.CardContentContainer(margin="12px")

        # Time and activity
        time_panel = FlowPanel(spacing="small")
        time_panel.add_component(
            Label(
                text=item.get("time", ""), font_size=13, bold=True, foreground="#1976d2"
            )
        )
        time_panel.add_component(Label(text=item.get("activity", ""), font_size=13))
        item_content.add_component(time_panel)

        # Responsible party
        if item.get("responsible_party"):
            item_content.add_component(
                Label(
                    text=f"👤 {item['responsible_party']}",
                    font_size=11,
                    foreground="#666",
                    spacing_above="tiny",
                )
            )

        item_card.add_component(item_content)
        return item_card

    # ========================================================================
    # ACTION BUTTONS
    # ========================================================================

    def add_action_buttons(self):
        """Add action buttons at bottom"""

        button_panel = FlowPanel(
            spacing="medium",
            align="center",
            spacing_above="large",
            spacing_below="medium",
        )

        # Back button
        back_btn = m3.Button(
            text=" Back to Events", icon="mi:arrow_back", appearance="outlined"
        )
        back_btn.set_event_handler("click", lambda **e: open_form("Events"))
        button_panel.add_component(back_btn)

        # Edit button
        edit_btn = m3.Button(text="Edit Event", icon="mi:edit", appearance="outlined")
        edit_btn.set_event_handler("click", self.edit_event_details)
        button_panel.add_component(edit_btn)

        # Export PDF button
        export_btn = m3.Button(
            text="Export PDF", icon="mi:picture_as_pdf", appearance="outlined"
        )
        export_btn.set_event_handler("click", self.export_pdf)
        button_panel.add_component(export_btn)

        # Share button
        share_btn = m3.Button(text="Share", icon="mi:share", appearance="filled")
        share_btn.set_event_handler("click", self.share_event)
        button_panel.add_component(share_btn)

        self.column_panel_main.add_component(button_panel)

    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    def toggle_task_complete(self, **event_args):
        """Toggle task completion"""
        sender = event_args["sender"]
        task_id = sender.tag.task_id
        is_done = sender.checked

        try:
            result = anvil.server.call("update_task_status", task_id, is_done)
            if result["success"]:
                Notification(
                    "Task updated!" if is_done else "Task marked incomplete",
                    timeout=2,
                    style="success",
                ).show()
                # Reload to refresh UI
                self.load_event_data()
            else:
                alert(f"Error: {result.get('error')}", title="Error")
                sender.checked = not is_done  # Revert
        except Exception as e:
            print(f"Error updating task: {e}")
            alert(f"Failed to update task: {str(e)}", title="Error")
            sender.checked = not is_done  # Revert

    def edit_event_details(self, **event_args):
        """Open edit dialog"""
        alert("Edit functionality coming soon!", title="Edit Event")

    def add_new_task(self, **event_args):
        """Add new task dialog"""
        alert("Add task functionality coming soon!", title="Add Task")

    def add_budget_item(self, **event_args):
        """Add budget item dialog"""
        alert("Add budget item functionality coming soon!", title="Add Budget Item")

    def export_pdf(self, **event_args):
        """Export event to PDF"""
        Notification("Generating PDF...", timeout=3).show()
        # TODO: Implement PDF export

    def share_event(self, **event_args):
        """Share event"""
        # TODO: Implement sharing functionality
        alert("Share functionality coming soon!", title="Share Event")

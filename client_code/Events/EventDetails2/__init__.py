# Events/EventView/__init__.py

from ._anvil_designer import EventDetails2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.users
from anvil.tables import app_tables
from datetime import datetime, timezone


class EventDetails2(EventDetails2Template):
    def __init__(self, event_id=24, **properties):
        self.init_components(**properties)

        self.event_id = event_id
        self.event_data = None

        if event_id:
            self.load_event_data()
        else:
            alert("No event ID provided", title="Error")
            open_form("Events.EventsList")

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
                    open_form("Events.EventsList")
            except Exception as e:
                print(f"Error loading event: {e}")
                alert(f"Failed to load event: {str(e)}", title="Error")
                open_form("Events.EventsList")

    def render_event_view(self):
        """Render the complete event view - MOBILE-FIRST"""

        # Clear container
        self.column_panel_main.clear()

        # Apply mobile-first role
        self.column_panel_main.role = "mobile-page"

        # Sticky Header Section
        self.add_event_header()

        # Scrollable content area
        content_area = ColumnPanel(spacing="medium", role="scrollable-content")

        # Quick Stats Row
        content_area.add_component(self.create_quick_stats())

        # Main Content - Single Column on Mobile, Two Columns on Desktop
        content_grid = FlowPanel(spacing="medium", align="left", role="responsive-grid")

        # Left Column (60% on desktop, 100% on mobile)
        left_column = ColumnPanel(spacing="medium", role="main-column")

        # Event Details Card (with accordion)
        left_column.add_component(self.create_event_details_card())

        # Selected Options Card (with accordion)
        if self.event_data.get("event_options"):
            left_column.add_component(self.create_selected_options_card())

        # AI Plan Sections (with accordions)
        if self.event_data.get("ai_response"):
            left_column.add_component(self.create_ai_plan_sections())

        content_grid.add_component(left_column, width="60%")

        # Right Column (40% on desktop, 100% on mobile)
        right_column = ColumnPanel(spacing="medium", role="sidebar-column")

        # Tasks Card (with accordion)
        right_column.add_component(self.create_tasks_card())

        # Budget Card (with accordion)
        right_column.add_component(self.create_budget_card())

        # Timeline Card (with accordion)
        right_column.add_component(self.create_timeline_card())

        content_grid.add_component(right_column, width="40%")

        content_area.add_component(content_grid)
        self.column_panel_main.add_component(content_area)

        # Fixed Bottom Action Buttons
        self.add_action_buttons()

    # ========================================================================
    # ACCORDION HELPER (Proven Pattern from ai_ui_builder)
    # ========================================================================

    def create_accordion_container(self, title, initially_open=False, color="#1976d2"):
        """
        Create accordion header and content panel with toggle
        Returns: (header_container, header_btn, content_panel)
        """

        # Header container
        header_container = ColumnPanel(
            background="theme:Surface Variant"
            if initially_open
            else "theme:Surface Container",
            spacing_above="none",
            spacing_below="none",
            role="accordion-header-container",
        )

        # Header button
        header_btn = m3.Link(
            text=title,
            align="left",
            icon="mi:expand_more" if initially_open else "mi:chevron_right",
            icon_size="18px",
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
            visible=initially_open,
            spacing_above="none",
            spacing_below="none",
            role="accordion-content",
        )

        # Toggle functionality
        is_expanded = {"value": initially_open}

        def toggle(**event_args):
            is_expanded["value"] = not is_expanded["value"]
            content_panel.visible = is_expanded["value"]
            header_btn.icon = (
                "mi:expand_more" if is_expanded["value"] else "mi:chevron_right"
            )

            if is_expanded["value"]:
                header_btn.background = "theme:Surface Variant"
                header_btn.role = "filled-button"
            else:
                header_btn.background = ""
                header_btn.role = None

        header_btn.set_event_handler("click", toggle)

        return (header_container, header_btn, content_panel)

    # ========================================================================
    # HEADER SECTION (Sticky on Mobile)
    # ========================================================================

    def add_event_header(self):
        """Add event header with title and status - STICKY"""

        header = ColumnPanel(
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            spacing="medium",
            role="event-header",
        )

        # Title row
        title_row = FlowPanel(spacing="medium", align="left")

        title_row.add_component(
            Label(
                text=self.event_data["title"],
                font_size=28,
                bold=True,
                foreground="black",
            )
        )

        # Status badge
        status = self.event_data.get("status", "planning")
        status_badge = Label(
            text=status.upper(),
            role=f"status-{status}",
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
                    foreground="black",
                    italic=True,
                )
            )

        # Date & Location row
        info_row = FlowPanel(spacing="large", align="left", role="header-info-row")

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
                    foreground="black",
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
                    text=location["formatted_address"], font_size=14, foreground="black"
                )
            )
            info_row.add_component(loc_panel)

        header.add_component(info_row)

        self.column_panel_main.add_component(header)

    # ========================================================================
    # QUICK STATS (Responsive Cards)
    # ========================================================================

    def create_quick_stats(self):
        """Add quick stats cards - RESPONSIVE"""

        stats_panel = FlowPanel(spacing="medium", align="left", role="stats-row")

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

        return stats_panel

    def create_stat_card(self, icon, value, label, color):
        """Create a stat card - MOBILE OPTIMIZED"""

        card = m3.Card(appearance="elevated", role="stat-card")
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
    # EVENT DETAILS CARD (With Accordion)
    # ========================================================================

    def create_event_details_card(self):
        """Event details card with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="📋 Event Details", initially_open=True, color="#1976d2"
        )

        # Edit button in header
        edit_btn = m3.Button(
            text="Edit",
            icon="mi:edit",
            appearance="outlined",
            size="small",
            role="inline-action-btn",
        )
        edit_btn.set_event_handler("click", self.edit_event_details)
        header_container.add_component(edit_btn)

        # Content
        details_content = ColumnPanel(spacing="small", role="section-content-padding")

        # Venue Type
        details_content.add_component(
            self.create_detail_row(
                "🏢 Venue Type:", self.event_data.get("venue_type", "Not specified")
            )
        )

        # Event Setting
        details_content.add_component(
            self.create_detail_row(
                "🎭 Setting:", self.event_data.get("event_setting", "Not specified")
            )
        )

        # Food & Beverage
        details_content.add_component(
            self.create_detail_row(
                "🍽️ Food & Beverage:", "Yes" if self.event_data.get("food_bev") else "No"
            )
        )

        # Created
        created_at = self.event_data.get("created_at")
        if created_at:
            details_content.add_component(
                self.create_detail_row(
                    "📅 Created:",
                    created_at.strftime("%B %d, %Y")
                    if hasattr(created_at, "strftime")
                    else str(created_at),
                )
            )

        content_panel.add_component(details_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_detail_row(self, label, value):
        """Create a detail row"""
        row = FlowPanel(spacing="small", align="left", role="detail-row")
        row.add_component(Label(text=label, bold=True, font_size=13, foreground="#666"))
        row.add_component(Label(text=str(value), font_size=13))
        return row

    # ========================================================================
    # SELECTED OPTIONS CARD (With Accordion)
    # ========================================================================

    def create_selected_options_card(self):
        """Selected options from AI with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="⭐ Your Selected Options", initially_open=False, color="#7b1fa2"
        )

        # Content
        options_content = ColumnPanel(spacing="medium", role="section-content-padding")

        options = self.event_data["event_options"]

        # Render each selected option
        for section_key, selection in options.items():
            section_title = section_key.replace("_", " ").title()

            # Section header
            options_content.add_component(
                Label(
                    text=section_title,
                    font_size=15,
                    bold=True,
                    foreground="#9c27b0",
                )
            )

            # Selection content
            if isinstance(selection, dict):
                options_content.add_component(
                    self.create_option_display_card(selection)
                )
            elif isinstance(selection, list):
                for item in selection:
                    options_content.add_component(self.create_option_display_card(item))

        content_panel.add_component(options_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_option_display_card(self, option):
        """Create display card for selected option"""

        card = m3.Card(appearance="outlined", spacing_above="small")
        card_content = m3.CardContentContainer(margin="12px")

        # Show key fields
        for key, value in option.items():
            if key in ["name", "style", "title"]:
                card_content.add_component(
                    Label(text=value, font_size=14, bold=True, foreground="#673ab7")
                )
            elif key == "description":
                card_content.add_component(
                    Label(text=value, font_size=12, spacing_above="tiny")
                )
            elif isinstance(value, list) and len(value) < 5:
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
    # AI PLAN SECTIONS (With Accordions)
    # ========================================================================

    def create_ai_plan_sections(self):
        """AI plan sections with accordions"""

        container = ColumnPanel(spacing="medium")

        ai_response = self.event_data.get("ai_response", {})
        plan = ai_response.get("plan", {})

        # Decorations
        if "decorations" in plan:
            container.add_component(
                self.create_decorations_section(plan["decorations"])
            )

        # Logistics
        if "logistics" in ai_response:
            container.add_component(
                self.create_simple_section("🚚 Logistics", ai_response["logistics"])
            )

        # Contingency Plans
        if "contingency_notes" in ai_response:
            container.add_component(
                self.create_simple_section(
                    "🛡️ Contingency Plans", ai_response["contingency_notes"]
                )
            )

        return container

    def create_decorations_section(self, decorations):
        """Decorations section with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="🎈 Decorations", initially_open=False, color="#e91e63"
        )

        # Content
        dec_content = ColumnPanel(spacing="small", role="section-content-padding")

        # Essential items
        if "essential_items" in decorations:
            dec_content.add_component(
                Label(
                    text="Essential Items:",
                    bold=True,
                    font_size=14,
                    foreground="#d32f2f",
                )
            )
            for item in decorations["essential_items"]:
                dec_content.add_component(self.create_bullet_item(item, "🔴"))

        # Optional items
        if "optional_items" in decorations and decorations["optional_items"]:
            dec_content.add_component(
                Label(
                    text="Optional Items:",
                    bold=True,
                    font_size=14,
                    spacing_above="small",
                    foreground="#1976d2",
                )
            )
            for item in decorations["optional_items"]:
                dec_content.add_component(self.create_bullet_item(item, "🔵"))

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
            dec_content.add_component(tip_card)

        content_panel.add_component(dec_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_simple_section(self, title, items):
        """Simple list section with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title=title, initially_open=False, color="#3f51b5"
        )

        # Content
        list_content = ColumnPanel(spacing="tiny", role="section-content-padding")

        if isinstance(items, list):
            for item in items:
                list_content.add_component(self.create_bullet_item(item))
        else:
            list_content.add_component(Label(text=str(items), font_size=13))

        content_panel.add_component(list_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_bullet_item(self, text, icon="•"):
        """Create bullet item"""
        row = FlowPanel(spacing="tiny", spacing_above="tiny")
        row.add_component(Label(text=icon, font_size=14))
        row.add_component(Label(text=str(text), font_size=13))
        return row

    # ========================================================================
    # TASKS CARD (With Accordion)
    # ========================================================================

    def create_tasks_card(self):
        """Tasks management card with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        tasks = self.event_data.get("tasks", [])
        completed_tasks = sum(1 for t in tasks if t.get("is_done"))

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title=f"✓ Tasks ({completed_tasks}/{len(tasks)})",
            initially_open=True,
            color="#ff9800",
        )

        # Add task button in header
        add_btn = m3.Button(
            text="Add",
            icon="mi:add",
            appearance="outlined",
            size="small",
            role="inline-action-btn",
        )
        add_btn.set_event_handler("click", self.add_new_task)
        header_container.add_component(add_btn)

        # Content
        tasks_content = ColumnPanel(spacing="small", role="section-content-padding")

        if not tasks:
            tasks_content.add_component(
                Label(
                    text="No tasks yet. Click Add to create one.",
                    font_size=13,
                    italic=True,
                    foreground="#999",
                )
            )
        else:
            for task in tasks:
                tasks_content.add_component(self.create_task_card(task))

        content_panel.add_component(tasks_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_task_card(self, task):
        """Create individual task card"""

        task_card = m3.Card(
            appearance="filled" if not task.get("is_done") else "outlined",
            spacing_above="small",
        )
        task_content = m3.CardContentContainer(margin="12px")

        # Task row
        task_row = FlowPanel(spacing="small", align="left", role="task-item")

        # Checkbox
        checkbox = CheckBox(checked=task.get("is_done", False), role="task-checkbox")
        checkbox.tag.task_id = task["id"]
        checkbox.set_event_handler("change", self.toggle_task_complete)
        task_row.add_component(checkbox)

        # Task text
        task_text = Label(
            text=task["task"],
            font_size=14,
            bold=not task.get("is_done"),
            foreground="#999" if task.get("is_done") else "#000",
            role="task-title",
        )
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
    # BUDGET CARD (With Accordion)
    # ========================================================================

    def create_budget_card(self):
        """Budget tracking card with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="💰 Budget", initially_open=False, color="#4caf50"
        )

        # Add item button in header
        add_btn = m3.Button(
            text="Add",
            icon="mi:add",
            appearance="outlined",
            size="small",
            role="inline-action-btn",
        )
        add_btn.set_event_handler("click", self.add_budget_item)
        header_container.add_component(add_btn)

        # Content
        budget_content = ColumnPanel(spacing="small", role="section-content-padding")

        budget = self.event_data.get("budget", 0)
        budget_items = self.event_data.get("budget_items", [])

        # Calculate totals
        estimated_total = sum(item.get("estimated_amount", 0) for item in budget_items)
        actual_total = sum(item.get("actual_amount", 0) for item in budget_items)

        # Total card
        total_card = m3.Card(appearance="filled", role="budget-summary")
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
        budget_content.add_component(total_card)

        # Budget items
        if not budget_items:
            budget_content.add_component(
                Label(
                    text="No budget items yet.",
                    font_size=13,
                    italic=True,
                    foreground="#999",
                    spacing_above="small",
                )
            )
        else:
            for item in budget_items:
                budget_content.add_component(self.create_budget_item_card(item))

        content_panel.add_component(budget_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_budget_item_card(self, item):
        """Create budget item card"""

        item_card = m3.Card(
            appearance="outlined", spacing_above="small", role="budget-item"
        )
        item_content = m3.CardContentContainer(margin="12px")

        # Header
        header = FlowPanel(spacing="small", align="left")
        header.add_component(Label(text=item["category"], font_size=13, bold=True))

        # Paid badge
        if item.get("paid"):
            header.add_component(Label(text="PAID", role="paid-badge"))

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
    # TIMELINE CARD (With Accordion)
    # ========================================================================

    def create_timeline_card(self):
        """Event timeline card with accordion"""

        section = ColumnPanel(role="collapsible-section", spacing="none")

        # Accordion
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="⏰ Timeline", initially_open=False, color="#1976d2"
        )

        # Content
        timeline_content = ColumnPanel(spacing="small", role="section-content-padding")

        # Get timeline from AI response
        ai_response = self.event_data.get("ai_response", {})
        timeline = ai_response.get("plan", {}).get("timeline", [])

        if not timeline:
            timeline_content.add_component(
                Label(
                    text="No timeline available.",
                    font_size=13,
                    italic=True,
                    foreground="#999",
                )
            )
        else:
            for i, item in enumerate(timeline):
                timeline_content.add_component(self.create_timeline_item(item, i))

        content_panel.add_component(timeline_content)

        # Assemble
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section.add_component(card_content)
        return section

    def create_timeline_item(self, item, index):
        """Create timeline item"""

        item_card = m3.Card(
            appearance="filled" if index % 2 == 0 else "outlined",
            spacing_above="small" if index > 0 else "none",
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
    # ACTION BUTTONS (Fixed Bottom Bar on Mobile)
    # ========================================================================

    def add_action_buttons(self):
        """Add action buttons - FIXED BOTTOM BAR on mobile"""

        button_panel = FlowPanel(
            spacing="small", align="left", role="bottom-action-bar"
        )

        # Back button
        back_btn = m3.Button(
            text="Back",
            icon="mi:arrow_back",
            appearance="outlined",
            role="action-button",
        )
        back_btn.set_event_handler("click", lambda **e: open_form("Events.EventsList"))
        button_panel.add_component(back_btn)

        # Edit button
        edit_btn = m3.Button(
            text="Edit", icon="mi:edit", appearance="outlined", role="action-button"
        )
        edit_btn.set_event_handler("click", self.edit_event_details)
        button_panel.add_component(edit_btn)

        # Export PDF button
        export_btn = m3.Button(
            text="PDF",
            icon="mi:picture_as_pdf",
            appearance="outlined",
            role="action-button",
        )
        export_btn.set_event_handler("click", self.export_pdf)
        button_panel.add_component(export_btn)

        # Share button
        share_btn = m3.Button(
            text="Share",
            icon="mi:share",
            appearance="filled",
            role="action-button-primary",
        )
        share_btn.set_event_handler("click", self.share_event)
        button_panel.add_component(share_btn)

        self.column_panel_main.add_component(button_panel)

    # ========================================================================
    # EVENT HANDLERS (All Preserved)
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
                self.load_event_data()
            else:
                alert(f"Error: {result.get('error')}", title="Error")
                sender.checked = not is_done
        except Exception as e:
            print(f"Error updating task: {e}")
            alert(f"Failed to update task: {str(e)}", title="Error")
            sender.checked = not is_done

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

    def share_event(self, **event_args):
        """Share event"""
        alert("Share functionality coming soon!", title="Share Event")

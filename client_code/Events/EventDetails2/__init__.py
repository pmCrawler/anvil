# Events/EventView/__init__.py

from ._anvil_designer import EventDetails2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.users
import m3.components as m3
from anvil.tables import app_tables
from datetime import datetime, timezone


class EventDetails2(EventDetails2Template):
    def __init__(self, event_id=None, **properties):
        self.init_components(**properties)

        self.event_id = event_id
        self.event_data = None

        # Configure mobile-first layout
        self.column_panel_main.role = "mobile-page"

        if event_id:
            self.load_event_data()
        else:
            alert("No event ID provided", title="Error")
            open_form("Events.EventsList")

    def load_event_data(self):
        """Load event data from server with loading state"""

        # Show loading skeleton
        self.show_loading_skeleton()

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

    def show_loading_skeleton(self):
        """Show loading skeleton while data loads"""
        self.column_panel_main.clear()

        skeleton = ColumnPanel(spacing="medium", role="scrollable-content")

        # Skeleton header
        skeleton.add_component(Label(text="", role="skeleton skeleton-title"))
        skeleton.add_component(Label(text="", role="skeleton skeleton-text"))
        skeleton.add_component(Label(text="", role="skeleton skeleton-text-short"))

        # Skeleton cards
        for i in range(3):
            skeleton.add_component(Label(text="", role="skeleton skeleton-card"))

        self.column_panel_main.add_component(skeleton)

    def render_event_view(self):
        """Render the complete mobile-first event view"""

        # Clear container
        self.column_panel_main.clear()

        # Sticky Header
        self.add_sticky_header()

        # Scrollable Content Area
        content_scroll = ColumnPanel(spacing="medium", role="scrollable-content")

        # Quick Stats Cards
        content_scroll.add_component(self.create_stats_row())

        # Collapsible Sections (Most Important First)
        content_scroll.add_component(self.create_overview_section())
        content_scroll.add_component(self.create_tasks_section())
        content_scroll.add_component(self.create_budget_section())
        content_scroll.add_component(self.create_timeline_section())

        # AI Plan Sections
        if self.event_data.get("ai_response"):
            content_scroll.add_component(self.create_selections_section())
            content_scroll.add_component(self.create_decorations_section())
            content_scroll.add_component(self.create_logistics_section())

        self.column_panel_main.add_component(content_scroll)

        # Fixed Bottom Action Bar
        self.add_bottom_action_bar()

    # ========================================================================
    # STICKY HEADER
    # ========================================================================

    def add_sticky_header(self):
        """Compact sticky header with essential info"""

        header = ColumnPanel(spacing="small", role="event-header")

        # Title row
        title_row = FlowPanel(spacing="small", align="left")

        # Event title (truncated for mobile)
        title = self.event_data["title"]
        if len(title) > 30:
            title = title[:27] + "..."

        title_label = Label(text=title, font_size=18, bold=True)
        title_label.role = "headline"
        title_row.add_component(title_label)

        # Status badge
        status = self.event_data.get("status", "planning")
        status_badge = Label(text=status.upper(), role=f"status-{status}")
        title_row.add_component(status_badge)

        header.add_component(title_row)

        # Date and countdown row
        event_date = self.event_data.get("event_datetime")
        if event_date:
            date_row = FlowPanel(spacing="small", align="left")

            # Date
            date_str = (
                event_date.strftime("%b %d, %Y")
                if hasattr(event_date, "strftime")
                else str(event_date)
            )
            date_row.add_component(Label(text=f"📅 {date_str}", font_size=13))

            # Countdown
            if isinstance(event_date, str):
                event_date = datetime.fromisoformat(event_date.replace("Z", "+00:00"))

            days_until = (event_date - datetime.now(timezone.utc)).days

            if days_until >= 0:
                countdown = Label(text=f"{days_until}d away", role="countdown")
                date_row.add_component(countdown)

            header.add_component(date_row)

        self.column_panel_main.add_component(header)

    # ========================================================================
    # STATS ROW
    # ========================================================================

    def create_stats_row(self):
        """Compact stats cards for mobile"""

        stats = FlowPanel(spacing="small", role="stats-row")

        # Guests
        stats.add_component(
            self.create_stat_mini(
                "👥", str(self.event_data.get("guest_count", 0)), "Guests"
            )
        )

        # Budget
        budget = self.event_data.get("budget", 0)
        stats.add_component(
            self.create_stat_mini("💰", f"${budget:,.0f}" if budget else "$0", "Budget")
        )

        # Tasks
        tasks = self.event_data.get("tasks", [])
        completed = sum(1 for t in tasks if t.get("is_done"))
        stats.add_component(
            self.create_stat_mini("✓", f"{completed}/{len(tasks)}", "Tasks")
        )

        return stats

    def create_stat_mini(self, icon, value, label):
        """Create compact stat card"""

        card = m3.Card(appearance="filled", role="stat-mini")
        content = ColumnPanel(spacing="tiny")

        content.add_component(Label(text=icon, font_size=20, align="center"))
        content.add_component(
            Label(text=value, font_size=16, bold=True, align="center")
        )
        content.add_component(
            Label(text=label, font_size=11, align="center", foreground="#666")
        )

        card.add_component(content)
        return card

    # ========================================================================
    # ACCORDION HELPER (Same pattern as ai_ui_builder.py)
    # ========================================================================

    def create_accordion_container(self, title, initially_open=False, color="#1976d2"):
        """
        Create accordion header and content panel with toggle
        SAME PATTERN AS ai_ui_builder.py

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

    # ========================================================================
    # COLLAPSIBLE SECTIONS (Using Working Accordion Pattern)
    # ========================================================================

    def create_overview_section(self):
        """Event overview - expanded by default"""

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="📋 Overview", initially_open=True, color="#1976d2"
        )

        # Add content
        content_panel.add_component(self.create_overview_content())

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    def create_tasks_section(self):
        """Tasks section - collapsed by default"""

        tasks = self.event_data.get("tasks", [])
        completed = sum(1 for t in tasks if t.get("is_done"))

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title=f"✓ Tasks ({completed}/{len(tasks)})",
            initially_open=False,
            color="#ff9800",
        )

        # Add content
        content_panel.add_component(self.create_tasks_content())

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    def create_budget_section(self):
        """Budget section - collapsed"""

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="💰 Budget", initially_open=False, color="#4caf50"
        )

        # Add content
        content_panel.add_component(self.create_budget_content())

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    def create_timeline_section(self):
        """Timeline section - collapsed"""

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="⏰ Timeline", initially_open=False, color="#1976d2"
        )

        # Add content
        content_panel.add_component(self.create_timeline_content())

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    def create_selections_section(self):
        """Selected options section"""

        if not self.event_data.get("event_options"):
            return ColumnPanel()

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="⭐ Your Selections", initially_open=False, color="#7b1fa2"
        )

        # Add content
        content_panel.add_component(self.create_selections_content())

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    def create_decorations_section(self):
        """Decorations section"""

        ai_response = self.event_data.get("ai_response", {})
        plan = ai_response.get("plan", {})

        if "decorations" not in plan:
            return ColumnPanel()

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="🎈 Decorations", initially_open=False, color="#e91e63"
        )

        # Add content
        content_panel.add_component(
            self.create_decorations_content(plan["decorations"])
        )

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    def create_logistics_section(self):
        """Logistics section"""

        ai_response = self.event_data.get("ai_response", {})

        if "logistics" not in ai_response:
            return ColumnPanel()

        # Create accordion
        section_container = ColumnPanel(role="collapsible-section", spacing="none")
        header_container, header_btn, content_panel = self.create_accordion_container(
            title="🚚 Logistics", initially_open=False, color="#3f51b5"
        )

        # Add content
        content_panel.add_component(
            self.create_logistics_content(ai_response["logistics"])
        )

        # Wrap in card
        card_content = m3.CardContentContainer(margin="0px")
        card_content.add_component(header_container)
        card_content.add_component(content_panel)

        section_container.add_component(card_content)
        return section_container

    # ========================================================================
    # SECTION CONTENT BUILDERS
    # ========================================================================

    def create_overview_content(self):
        """Build overview content"""

        panel = ColumnPanel(spacing="small", role="section-content-padding")

        # Description
        if self.event_data.get("description"):
            panel.add_component(
                Label(
                    text=self.event_data["description"], font_size=14, foreground="#444"
                )
            )

        # Details list
        details = ColumnPanel(spacing="tiny", spacing_above="medium")

        details.add_component(
            self.create_detail_row(
                "🏢", "Venue", self.event_data.get("venue_type", "Not specified")
            )
        )

        details.add_component(
            self.create_detail_row(
                "🎭", "Setting", self.event_data.get("event_setting", "Not specified")
            )
        )

        details.add_component(
            self.create_detail_row(
                "🍽️", "Food/Beverage", "Yes" if self.event_data.get("food_bev") else "No"
            )
        )

        # Location
        location = self.event_data.get("location")
        if location and location.get("formatted_address"):
            details.add_component(
                self.create_detail_row("📍", "Location", location["formatted_address"])
            )

        panel.add_component(details)

        return panel

    def create_tasks_content(self):
        """Build tasks list with checkboxes"""

        panel = ColumnPanel(spacing="small", role="section-content-padding")

        tasks = self.event_data.get("tasks", [])

        if not tasks:
            panel.add_component(
                Label(text="No tasks yet", font_size=14, italic=True, foreground="#999")
            )
            return panel

        # Progress bar
        completed = sum(1 for t in tasks if t.get("is_done"))
        total = len(tasks)
        percentage = (completed / total * 100) if total > 0 else 0

        progress_container = ColumnPanel(spacing="tiny", spacing_below="medium")
        progress_container.add_component(
            Label(
                text=f"{completed} of {total} complete", font_size=12, foreground="#666"
            )
        )

        # Progress bar visual
        bar_outer = ColumnPanel(role="progress-bar-track")
        bar_inner = Label(text="", role="progress-bar-fill")
        bar_inner.tag.width = f"{percentage}%"
        bar_outer.add_component(bar_inner)
        progress_container.add_component(bar_outer)

        panel.add_component(progress_container)

        # Task list
        for task in tasks:
            task_item = self.create_task_item(task)
            panel.add_component(task_item)

        return panel

    def create_task_item(self, task):
        """Create individual task item"""

        item = FlowPanel(spacing="small", role="task-item")

        # Checkbox
        checkbox = CheckBox(checked=task.get("is_done", False), role="task-checkbox")
        checkbox.tag.task_id = task["id"]
        checkbox.set_event_handler("change", self.toggle_task_complete)
        item.add_component(checkbox)

        # Task info column
        task_info = ColumnPanel(spacing="tiny")

        # Task text
        task_text = Label(
            text=task["task"],
            font_size=15,
            bold=not task.get("is_done"),
            foreground="#999" if task.get("is_done") else "#000",
            role="task-title",
        )
        task_info.add_component(task_text)

        # Due date
        if task.get("due_date"):
            due_date = task["due_date"]
            due_str = (
                due_date.strftime("%b %d")
                if hasattr(due_date, "strftime")
                else str(due_date)
            )
            task_info.add_component(
                Label(text=f"Due: {due_str}", font_size=12, foreground="#666")
            )

        item.add_component(task_info)

        return item

    def create_budget_content(self):
        """Build budget breakdown"""

        panel = ColumnPanel(spacing="small", role="section-content-padding")

        budget = self.event_data.get("budget", 0)
        budget_items = self.event_data.get("budget_items", [])

        # Summary card
        summary = m3.Card(appearance="filled", role="budget-summary")
        summary_content = ColumnPanel(spacing="tiny")

        estimated_total = sum(item.get("estimated_amount", 0) for item in budget_items)
        actual_total = sum(item.get("actual_amount", 0) for item in budget_items)

        summary_content.add_component(
            Label(
                text=f"Total Budget: ${budget:,.0f}",
                font_size=18,
                bold=True,
                foreground="#2e7d32",
            )
        )

        if budget_items:
            summary_content.add_component(
                Label(
                    text=f"Estimated: ${estimated_total:,.0f}",
                    font_size=13,
                    foreground="#666",
                )
            )

            if budget > 0:
                percentage = estimated_total / budget * 100
                color = "#f44336" if percentage > 100 else "#4caf50"
                summary_content.add_component(
                    Label(
                        text=f"{percentage:.0f}% allocated",
                        font_size=13,
                        foreground=color,
                        bold=True,
                    )
                )

        summary.add_component(summary_content)
        panel.add_component(summary)

        # Budget items
        if budget_items:
            for item in budget_items:
                panel.add_component(self.create_budget_item_card(item))
        else:
            panel.add_component(
                Label(
                    text="No budget items yet",
                    font_size=14,
                    italic=True,
                    foreground="#999",
                    spacing_above="small",
                )
            )

        return panel

    def create_budget_item_card(self, item):
        """Create budget item card"""

        card = m3.Card(appearance="outlined", role="budget-item", spacing_above="small")
        content = ColumnPanel(spacing="tiny")

        # Header row
        header = FlowPanel(spacing="small", align="left")
        header.add_component(Label(text=item["category"], font_size=14, bold=True))

        if item.get("paid"):
            header.add_component(Label(text="PAID", role="paid-badge"))

        content.add_component(header)

        # Amount
        estimated = item.get("estimated_amount", 0)
        content.add_component(
            Label(
                text=f"${estimated:,.2f}", font_size=15, bold=True, foreground="#4caf50"
            )
        )

        card.add_component(content)
        return card

    def create_timeline_content(self):
        """Build timeline"""

        panel = ColumnPanel(spacing="small", role="section-content-padding")

        ai_response = self.event_data.get("ai_response", {})
        timeline = ai_response.get("plan", {}).get("timeline", [])

        if not timeline:
            panel.add_component(
                Label(
                    text="No timeline available",
                    font_size=14,
                    italic=True,
                    foreground="#999",
                )
            )
            return panel

        for i, item in enumerate(timeline):
            timeline_card = m3.Card(
                appearance="filled" if i % 2 == 0 else "outlined",
                spacing_above="tiny" if i > 0 else "none",
            )
            timeline_content = ColumnPanel(spacing="tiny")

            # Time and activity
            timeline_content.add_component(
                Label(
                    text=f"{item.get('time', '')} - {item.get('activity', '')}",
                    font_size=14,
                    bold=True,
                )
            )

            # Responsible party
            if item.get("responsible_party"):
                timeline_content.add_component(
                    Label(
                        text=f"👤 {item['responsible_party']}",
                        font_size=12,
                        foreground="#666",
                    )
                )

            timeline_card.add_component(timeline_content)
            panel.add_component(timeline_card)

        return panel

    def create_selections_content(self):
        """Build selected options"""

        panel = ColumnPanel(spacing="medium", role="section-content-padding")

        options = self.event_data["event_options"]

        for section_key, selection in options.items():
            section_title = section_key.replace("_", " ").title()

            # Section header
            panel.add_component(
                Label(text=section_title, font_size=15, bold=True, foreground="#7b1fa2")
            )

            # Selection cards
            if isinstance(selection, dict):
                panel.add_component(self.create_selection_card(selection))
            elif isinstance(selection, list):
                for item in selection:
                    panel.add_component(self.create_selection_card(item))

        return panel

    def create_selection_card(self, option):
        """Create selection display card"""

        card = m3.Card(appearance="outlined", spacing_above="tiny")
        content = ColumnPanel(spacing="tiny")

        # Show main field
        for key, value in option.items():
            if key in ["name", "style", "title"]:
                content.add_component(Label(text=value, font_size=14, bold=True))
            elif key == "description":
                content.add_component(
                    Label(text=value, font_size=13, foreground="#666")
                )

        card.add_component(content)
        return card

    def create_decorations_content(self, decorations):
        """Build decorations section"""

        panel = ColumnPanel(spacing="small", role="section-content-padding")

        # Essential items
        if "essential_items" in decorations:
            panel.add_component(
                Label(text="Essential:", bold=True, foreground="#d32f2f")
            )
            for item in decorations["essential_items"]:
                panel.add_component(Label(text=f"• {item}", font_size=13))

        # Optional items
        if decorations.get("optional_items"):
            panel.add_component(
                Label(
                    text="Optional:",
                    bold=True,
                    foreground="#1976d2",
                    spacing_above="small",
                )
            )
            for item in decorations["optional_items"]:
                panel.add_component(Label(text=f"• {item}", font_size=13))

        return panel

    def create_logistics_content(self, logistics):
        """Build logistics section"""

        panel = ColumnPanel(spacing="tiny", role="section-content-padding")

        if isinstance(logistics, list):
            for item in logistics:
                panel.add_component(Label(text=f"• {item}", font_size=13))
        else:
            panel.add_component(Label(text=str(logistics), font_size=13))

        return panel

    # ========================================================================
    # HELPERS
    # ========================================================================

    def create_detail_row(self, icon, label, value):
        """Create detail row with icon"""

        row = FlowPanel(spacing="tiny", role="detail-row")
        row.add_component(Label(text=icon, font_size=16))
        row.add_component(
            Label(text=f"{label}:", bold=True, font_size=14, foreground="#666")
        )
        row.add_component(Label(text=str(value), font_size=14))
        return row

    # ========================================================================
    # BOTTOM ACTION BAR
    # ========================================================================

    def add_bottom_action_bar(self):
        """Fixed bottom action bar"""

        bar = FlowPanel(spacing="small", role="bottom-action-bar")

        # Back button
        back_btn = m3.Button(
            text="Back",
            icon="mi:arrow_back",
            appearance="outlined",
            role="action-button-secondary",
        )
        back_btn.set_event_handler("click", lambda **e: open_form("Events.EventsList"))
        bar.add_component(back_btn)

        # Primary action
        edit_btn = m3.Button(
            text="Edit Event",
            icon="mi:edit",
            appearance="filled",
            role="action-button-primary",
        )
        edit_btn.set_event_handler("click", self.edit_event)
        bar.add_component(edit_btn)

        self.column_panel_main.add_component(bar)

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
                    "✓ Task updated" if is_done else "Task incomplete",
                    timeout=2,
                    style="success",
                ).show()
                self.load_event_data()  # Reload to update counts
            else:
                alert(f"Error: {result.get('error')}", title="Error")
                sender.checked = not is_done
        except Exception as e:
            print(f"Error updating task: {e}")
            alert(f"Failed to update task: {str(e)}", title="Error")
            sender.checked = not is_done

    def edit_event(self, **event_args):
        """Edit event"""
        alert("Edit functionality coming soon!", title="Edit Event")

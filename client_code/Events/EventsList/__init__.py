# Events/__init__.py

from ._anvil_designer import EventsListTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.users
import m3.components as m3
from anvil.tables import app_tables
from datetime import datetime, timezone


class EventsList(EventsListTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        self.events = []
        self.filter_status = "all"
        self.sort_by = "date_desc"

        self.load_events()

    def load_events(self):
        """Load user's events from server"""

        # with Notification("Loading events...", timeout=None):
        try:
            result = anvil.server.call(
                "get_user_events",
                self.filter_status,
                self.sort_by,
            )

            if result["success"]:
                self.events = result["events"]
                self.render_event_list()
            else:
                alert(f"Error loading events: {result.get('error')}", title="Error")
        except Exception as e:
            print(f"Error loading events: {e}")
            alert(f"Failed to load events: {str(e)}", title="Error")

    def render_event_list(self):
        """Render the event list with filters and cards"""

        # Clear container
        self.column_panel_main.clear()

        # Add header
        self.add_header()

        # Add filters and actions bar
        self.add_filters_bar()

        # Add stats summary
        self.add_stats_summary()

        # Add events grid
        if not self.events:
            self.add_empty_state()
        else:
            self.add_events_grid()

    # ========================================================================
    # HEADER SECTION
    # ========================================================================

    def add_header(self):
        """Add page header"""

        header = ColumnPanel(
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            spacing="medium",
        )

        # Title row
        title_row = FlowPanel(spacing="medium", align="left")

        title_row.add_component(
            Label(text="🎉 My Events", font_size=28, bold=True, foreground="white")
        )

        # Create new event button
        create_btn = m3.Button(
            text="Create Event", icon="mi:add_circle", appearance="filled", size="large"
        )
        create_btn.background = "white"
        create_btn.foreground = "#667eea"
        create_btn.set_event_handler("click", self.create_new_event)
        title_row.add_component(create_btn)

        header.add_component(title_row)

        # Subtitle
        header.add_component(
            Label(
                text=f"Manage and track all your events in one place",
                font_size=15,
                foreground="white",
                italic=True,
            )
        )

        self.column_panel_main.add_component(header)

    # ========================================================================
    # FILTERS BAR
    # ========================================================================

    def add_filters_bar(self):
        """Add filters and sort options"""

        filters_panel = FlowPanel(
            spacing="medium",
            align="left",
            spacing_above="medium",
            spacing_below="medium",
        )

        # Status filter
        filters_panel.add_component(
            Label(text="Filter:", bold=True, font_size=14, foreground="#666")
        )

        status_options = [
            ("all", "All Events"),
            ("upcoming", "Upcoming"),
            ("planning", "Planning"),
            ("confirmed", "Confirmed"),
            ("completed", "Completed"),
        ]

        for value, label in status_options:
            filter_btn = m3.Button(
                text=label,
                appearance="filled" if self.filter_status == value else "outlined",
                size="small",
            )
            filter_btn.tag.filter_value = value
            filter_btn.set_event_handler("click", self.apply_filter)
            filters_panel.add_component(filter_btn)

        # Spacer
        filters_panel.add_component(Spacer(width=20))

        # Sort dropdown
        filters_panel.add_component(
            Label(text="Sort by:", bold=True, font_size=14, foreground="#666")
        )

        sort_dropdown = DropDown(
            items=[
                ("date_desc", "Date (Newest First)"),
                ("date_asc", "Date (Oldest First)"),
                ("title_asc", "Title (A-Z)"),
                ("created_desc", "Recently Created"),
                ("budget_desc", "Budget (High to Low)"),
            ],
            selected_value=self.sort_by,
        )
        sort_dropdown.set_event_handler("change", self.apply_sort)
        filters_panel.add_component(sort_dropdown)

        # Search box (future enhancement)
        search_box = TextBox(placeholder="🔍 Search events...", spacing_above="none")
        search_box.set_event_handler("pressed_enter", self.search_events)
        filters_panel.add_component(search_box)

        self.column_panel_main.add_component(filters_panel)

    # ========================================================================
    # STATS SUMMARY
    # ========================================================================

    def add_stats_summary(self):
        """Add quick stats about events"""

        stats_panel = FlowPanel(spacing="medium", align="left", spacing_below="medium")

        # Calculate stats
        total_events = len(self.events)
        upcoming_events = sum(1 for e in self.events if self.is_upcoming(e))
        planning_events = sum(1 for e in self.events if e.get("status") == "planning")
        total_budget = sum(e.get("budget", 0) for e in self.events)

        # Total Events
        stats_panel.add_component(
            self.create_mini_stat("📊", str(total_events), "Total Events")
        )

        # Upcoming
        stats_panel.add_component(
            self.create_mini_stat("📅", str(upcoming_events), "Upcoming")
        )

        # Planning
        stats_panel.add_component(
            self.create_mini_stat("✏️", str(planning_events), "In Planning")
        )

        # Total Budget
        stats_panel.add_component(
            self.create_mini_stat("💰", f"${total_budget:,.0f}", "Total Budget")
        )

        self.column_panel_main.add_component(stats_panel)

    def create_mini_stat(self, icon, value, label):
        """Create mini stat card"""

        stat_panel = FlowPanel(spacing="tiny", background="#f5f5f5")
        stat_panel.add_component(Label(text=icon, font_size=20))

        text_panel = ColumnPanel(spacing="none")
        text_panel.add_component(
            Label(text=value, font_size=18, bold=True, foreground="#1976d2")
        )
        text_panel.add_component(Label(text=label, font_size=11, foreground="#666"))

        stat_panel.add_component(text_panel)
        return stat_panel

    # ========================================================================
    # EVENTS GRID
    # ========================================================================

    def add_events_grid(self):
        """Add grid of event cards"""

        # Grid container (3 columns on desktop, responsive)
        grid = FlowPanel(spacing="medium", align="left")

        for event in self.events:
            event_card = self.create_event_card(event)
            grid.add_component(event_card, width="32%")

        self.column_panel_main.add_component(grid)

    def create_event_card(self, event):
        """
        Create comprehensive event card with all relevant info

        Card includes:
        - Status badge
        - Event title
        - Date & countdown
        - Location
        - Guest count
        - Budget
        - Progress indicators (tasks, budget)
        - Quick actions (View, Edit, Delete)
        """

        # Main card container
        card_container = ColumnPanel(
            spacing="none", spacing_above="none", spacing_below="small"
        )

        # Card
        card = m3.Card(appearance="outlined")
        card.role = "card"
        card_content = m3.CardContentContainer(margin="16px")

        # Status badge (top right)
        status = event.get("status", "planning")
        status_badge = self.create_status_badge(status)
        card_content.add_component(status_badge)

        # Event Title
        title = Label(
            text=event["title"], font_size=18, bold=True, foreground="#1976d2"
        )
        title.role = "headline"
        card_content.add_component(title)

        # Description (truncated)
        if event.get("description"):
            desc_text = event["description"]
            if len(desc_text) > 80:
                desc_text = desc_text[:77] + "..."

            card_content.add_component(
                Label(
                    text=desc_text,
                    font_size=12,
                    foreground="#666",
                    spacing_above="tiny",
                )
            )

        # Divider
        card_content.add_component(Spacer(height=8))

        # Date & Countdown
        event_datetime = event.get("event_datetime")
        if event_datetime:
            date_panel = self.create_date_section(event_datetime)
            card_content.add_component(date_panel)

        # Location
        location = event.get("location")
        if location and location.get("formatted_address"):
            loc_panel = FlowPanel(spacing="tiny", spacing_above="small")
            loc_panel.add_component(Label(text="📍", font_size=14))

            # Truncate long addresses
            address = location["formatted_address"]
            if len(address) > 40:
                address = address[:37] + "..."

            loc_panel.add_component(
                Label(text=address, font_size=12, foreground="#666")
            )
            card_content.add_component(loc_panel)

        # Info Row (Guests & Budget)
        info_row = FlowPanel(spacing="medium", spacing_above="medium")

        # Guest count
        guest_count = event.get("guest_count", 0)
        guest_panel = FlowPanel(spacing="tiny")
        guest_panel.add_component(Label(text="👥", font_size=14))
        guest_panel.add_component(
            Label(
                text=f"{guest_count} guests",
                font_size=12,
                bold=True,
                foreground="#2196f3",
            )
        )
        info_row.add_component(guest_panel)

        # Budget
        budget = event.get("budget", 0)
        if budget > 0:
            budget_panel = FlowPanel(spacing="tiny")
            budget_panel.add_component(Label(text="💰", font_size=14))
            budget_panel.add_component(
                Label(
                    text=f"${budget:,.0f}",
                    font_size=12,
                    bold=True,
                    foreground="#4caf50",
                )
            )
            info_row.add_component(budget_panel)

        card_content.add_component(info_row)

        # Progress Indicators
        progress_section = self.create_progress_section(event)
        if progress_section:
            card_content.add_component(progress_section)

        # Event Type Badge
        if event.get("ai_response"):
            event_classification = event["ai_response"].get("event_classification", "")
            if event_classification:
                type_badge = Label(
                    text=f"🎯 {event_classification}",
                    font_size=11,
                    foreground="#673ab7",
                    italic=True,
                    spacing_above="small",
                )
                card_content.add_component(type_badge)

        # Divider
        card_content.add_component(Spacer(height=8))

        # Action Buttons
        actions_row = FlowPanel(
            spacing="small",
            spacing_above="small",
        )

        # View Details button
        view_btn = m3.Button(
            text="Details",
            icon="mi:visibility",
            appearance="filled",
            size="tiny",
            align="center",
        )
        view_btn.tag.event_id = event["id"]
        view_btn.set_event_handler("click", self.view_event_details)
        actions_row.add_component(view_btn, width="100%")

        # # Edit button
        # edit_btn = m3.Button(
        #     text="Edit", icon="mi:edit", appearance="outlined", size="small"
        # )
        # edit_btn.tag.event_id = event["id"]
        # edit_btn.set_event_handler("click", self.edit_event)
        # actions_row.add_component(edit_btn)

        # # Delete button
        # delete_btn = m3.Button(
        #     text="", icon="mi:delete", appearance="outlined", size="small"
        # )
        # delete_btn.foreground = "#f44336"
        # delete_btn.tag.event_id = event["id"]
        # delete_btn.set_event_handler("click", self.delete_event)
        # actions_row.add_component(delete_btn)

        card_content.add_component(actions_row)

        # Make entire card clickable
        def card_click(**event_args):
            self.view_event_details(event_id=event["id"])

        card.set_event_handler("x-click", card_click)

        card.add_component(card_content)
        card_container.add_component(card)

        return card_container

    def create_status_badge(self, status):
        """Create status badge"""

        status_config = {
            "planning": {"text": "PLANNING", "bg": "#ff9800", "icon": "✏️"},
            "confirmed": {"text": "CONFIRMED", "bg": "#4caf50", "icon": "✓"},
            "completed": {"text": "COMPLETED", "bg": "#2196f3", "icon": "🎉"},
            "cancelled": {"text": "CANCELLED", "bg": "#f44336", "icon": "✗"},
        }

        config = status_config.get(
            status, {"text": status.upper(), "bg": "#757575", "icon": "•"}
        )

        badge_panel = FlowPanel(
            spacing="tiny",
            align="right",
            spacing_below="small",
        )
        badge = Label(
            text=f"{config['icon']} {config['text']}",
            font_size=10,
            bold=True,
            background=config["bg"],
            foreground="white",
        )
        badge_panel.add_component(badge)

        return badge_panel

    def create_date_section(self, event_datetime):
        """Create date section with countdown"""

        date_panel = ColumnPanel(spacing="tiny", spacing_above="small")

        # Format date
        if isinstance(event_datetime, str):
            try:
                event_datetime = datetime.fromisoformat(
                    event_datetime.replace("Z", "+00:00")
                )
            except:
                pass

        if hasattr(event_datetime, "strftime"):
            date_str = event_datetime.strftime("%B %d, %Y at %I:%M %p")
        else:
            date_str = str(event_datetime)

        # Date display
        date_row = FlowPanel(spacing="tiny")
        date_row.add_component(Label(text="📅", font_size=14))
        date_row.add_component(
            Label(text=date_str, font_size=12, bold=True, foreground="#1976d2")
        )
        date_panel.add_component(date_row)

        # Countdown
        if hasattr(event_datetime, "replace"):
            try:
                now = datetime.now(timezone.utc)
                if event_datetime.tzinfo is None:
                    event_datetime = event_datetime.replace(tzinfo=timezone.utc)

                delta = event_datetime - now
                days_until = delta.days

                countdown_text = ""
                countdown_color = "#666"

                if days_until < 0:
                    countdown_text = f"{abs(days_until)} days ago"
                    countdown_color = "#999"
                elif days_until == 0:
                    countdown_text = "📢 TODAY!"
                    countdown_color = "#f44336"
                elif days_until == 1:
                    countdown_text = "⚡ Tomorrow"
                    countdown_color = "#ff5722"
                elif days_until <= 7:
                    countdown_text = f"⏰ {days_until} days away"
                    countdown_color = "#ff9800"
                elif days_until <= 30:
                    countdown_text = f"📆 {days_until} days away"
                    countdown_color = "#2196f3"
                else:
                    countdown_text = f"🗓️ {days_until} days away"
                    countdown_color = "#9c27b0"

                countdown_label = Label(
                    text=countdown_text,
                    font_size=11,
                    bold=True if days_until <= 7 else False,
                    foreground=countdown_color,
                    spacing_above="tiny",
                )
                date_panel.add_component(countdown_label)
            except:
                pass

        return date_panel

    def create_progress_section(self, event):
        """Create progress indicators for tasks and budget"""

        tasks = event.get("tasks", [])
        budget_items = event.get("budget_items", [])

        if not tasks and not budget_items:
            return None

        progress_panel = ColumnPanel(spacing="tiny", spacing_above="medium")

        # Tasks progress
        if tasks:
            total_tasks = len(tasks)
            completed_tasks = sum(1 for t in tasks if t.get("is_done"))
            task_percentage = (
                (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            )

            task_row = FlowPanel(spacing="small", align="left")
            task_row.add_component(Label(text="✓", font_size=12, foreground="#4caf50"))
            task_row.add_component(
                Label(
                    text=f"Tasks: {completed_tasks}/{total_tasks}",
                    font_size=11,
                    foreground="#666",
                )
            )

            # Progress bar
            progress_bar = self.create_progress_bar(task_percentage, "#4caf50")

            task_col = ColumnPanel(spacing="tiny")
            task_col.add_component(task_row)
            task_col.add_component(progress_bar)

            progress_panel.add_component(task_col)

        # Budget progress
        budget = event.get("budget", 0)
        if budget_items and budget > 0:
            estimated_total = sum(
                item.get("estimated_amount", 0) for item in budget_items
            )
            budget_percentage = (
                min((estimated_total / budget * 100), 100) if budget > 0 else 0
            )

            budget_row = FlowPanel(spacing="small", align="left", spacing_above="small")
            budget_row.add_component(Label(text="💰", font_size=12))
            budget_row.add_component(
                Label(
                    text=f"Budget: ${estimated_total:,.0f} / ${budget:,.0f}",
                    font_size=11,
                    foreground="#666",
                )
            )

            # Progress bar (red if over budget)
            bar_color = "#f44336" if budget_percentage > 100 else "#4caf50"
            progress_bar = self.create_progress_bar(budget_percentage, bar_color)

            budget_col = ColumnPanel(spacing="tiny")
            budget_col.add_component(budget_row)
            budget_col.add_component(progress_bar)

            progress_panel.add_component(budget_col)

        return progress_panel

    def create_progress_bar(self, percentage, color):
        """Create progress bar"""

        bar_container = ColumnPanel(background="#e0e0e0", spacing="none")

        # Fill (cap at 100% visually)
        fill_width = min(percentage, 100)

        bar_fill = Label(
            text=f"  {percentage:.0f}%",
            background=color,
            foreground="white",
            font_size=9,
            bold=True,
        )

        bar_container.add_component(bar_fill)

        return bar_container

    # ========================================================================
    # EMPTY STATE
    # ========================================================================

    def add_empty_state(self):
        """Add empty state when no events"""

        empty_container = ColumnPanel(
            spacing="medium", spacing_above="large", spacing_below="large"
        )

        # Icon
        empty_container.add_component(Label(text="🎉", font_size=64, align="center"))

        # Message
        empty_container.add_component(
            Label(
                text="No events yet!",
                font_size=24,
                bold=True,
                align="center",
                foreground="#666",
            )
        )

        empty_container.add_component(
            Label(
                text="Create your first event to get started",
                font_size=14,
                align="center",
                foreground="#999",
            )
        )

        # Create button
        create_btn = m3.Button(
            text="Create Your First Event",
            icon="mi:add_circle",
            appearance="filled",
            size="large",
            align="center",
        )
        create_btn.set_event_handler("click", self.create_new_event)
        empty_container.add_component(create_btn)

        self.column_panel_main.add_component(empty_container)

    # ========================================================================
    # EVENT HANDLERS
    # ========================================================================

    def apply_filter(self, **event_args):
        """Apply status filter"""
        sender = event_args["sender"]
        self.filter_status = sender.tag.filter_value
        self.load_events()

    def apply_sort(self, **event_args):
        """Apply sort order"""
        sender = event_args["sender"]
        self.sort_by = sender.selected_value
        self.load_events()

    def search_events(self, **event_args):
        """Search events (future enhancement)"""
        search_text = event_args["sender"].text
        Notification(f"Searching for: {search_text}", timeout=2).show()
        # TODO: Implement search

    def view_event_details(self, event_id=None, **event_args):
        """Navigate to event details"""
        if event_id is None:
            event_id = event_args["sender"].tag.event_id

        open_form("Events.EventDetails", event_id=event_id)

    def edit_event(self, **event_args):
        """Edit event"""
        event_id = event_args["sender"].tag.event_id
        # TODO: Navigate to edit form
        Notification(f"Edit event {event_id}", timeout=2).show()

    def delete_event(self, **event_args):
        """Delete event with confirmation"""
        event_id = event_args["sender"].tag.event_id

        if confirm(
            "Are you sure you want to delete this event? This action cannot be undone.",
            title="Delete Event",
        ):
            try:
                result = anvil.server.call("delete_event", event_id)

                if result["success"]:
                    Notification(
                        "Event deleted successfully", timeout=3, style="success"
                    ).show()
                    self.load_events()  # Reload list
                else:
                    alert(f"Error deleting event: {result.get('error')}", title="Error")
            except Exception as e:
                print(f"Error deleting event: {e}")
                alert(f"Failed to delete event: {str(e)}", title="Error")

    def create_new_event(self, **event_args):
        """Navigate to create event form"""
        open_form("Events.EventForm")

    def is_upcoming(self, event):
        """Check if event is upcoming"""
        event_datetime = event.get("event_datetime")
        if not event_datetime:
            return False

        try:
            if isinstance(event_datetime, str):
                event_datetime = datetime.fromisoformat(
                    event_datetime.replace("Z", "+00:00")
                )

            now = datetime.now(timezone.utc)
            if event_datetime.tzinfo is None:
                event_datetime = event_datetime.replace(tzinfo=timezone.utc)

            return event_datetime > now
        except:
            return False

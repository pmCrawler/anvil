import json

import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.users
import m3.components as m3
from anvil import *
from anvil.tables import app_tables

from ._anvil_designer import AIResponseTemplate


class AIResponse(AIResponseTemplate):
    """Component for rendering AI response data as interactive accordions"""

    def __init__(self, resp=None, **properties):
        self.init_components(**properties)
        self.selected_values = {}

        ai_response = properties if resp is None else resp
        self.process_json_response(ai_response)

    def process_json_response(self, json_response):
        """Process JSON response and create dynamic controls"""
        self.cpanel_ai_resp.clear()
        self.selected_values = {}

        json_data = self._parse_json_response(json_response)
        if json_data is None:
            return

        main_container = self._create_main_container(json_data)
        self.cpanel_ai_resp.add_component(main_container)

    def _parse_json_response(self, json_response):
        """Parse and validate JSON response"""
        if isinstance(json_response, str):
            try:
                json_data = json.loads(json_response)
            except json.JSONDecodeError:
                alert("Invalid JSON format")
                return None
        else:
            json_data = json_response

        # Extract single item from list if needed
        if isinstance(json_data, list) and len(json_data) > 0:
            json_data = json_data[0]

        return json_data

    def _create_main_container(self, json_data):
        """Create the main container with all accordions"""
        main_container = ColumnPanel()

        for key, value in json_data.items():
            accordion_panel = self.create_accordion_section(key, value)
            if accordion_panel:
                main_container.add_component(accordion_panel)

        return main_container

    def create_accordion_section(self, key, value):
        """Create an accordion section for a root element"""
        accordion = ColumnPanel(
            spacing_above="none",
            spacing_below="none",
            wrap_on="mobile",
        )

        card = m3.Card(appearance="outlined", visible=False)
        content_panel = ColumnPanel(
            visible=False,
            spacing_above="none",
            wrap_on="mobile",
        )

        header_container, header_btn = self._create_accordion_header(key)
        self._setup_accordion_toggle(header_btn, content_panel, card, key)

        self._populate_content_panel(content_panel, value, key)

        # Assemble components
        card_content = m3.CardContentContainer(margin="16px")
        card_content.add_component(content_panel)
        card.add_component(card_content)

        accordion.add_component(header_container, full_width_row=True)
        accordion.add_component(card)

        return accordion

    def _create_accordion_header(self, key):
        """Create accordion header with button"""
        header_container = m3.Text(scale="small")
        header_btn = m3.Button(
            text=f"▶ {self.format_title(key)}",
            align="left",
            icon_align="left",
            appearance="tonal",
        )
        header_container.add_component(header_btn)
        return header_container, header_btn

    def _setup_accordion_toggle(self, header_btn, content_panel, card, key):
        """Setup accordion toggle functionality"""
        is_expanded = {"value": False}

        def toggle_accordion(**event_args):
            is_expanded["value"] = not is_expanded["value"]
            content_panel.visible = is_expanded["value"]
            card.visible = is_expanded["value"]

            arrow = "▼" if is_expanded["value"] else "▶"
            header_btn.text = f"{arrow} {self.format_title(key)}"

            if is_expanded["value"]:
                header_btn.background = "theme:Primary 100"
                header_btn.role = "filled-button"
            else:
                header_btn.background = "theme:Gray 50"
                header_btn.role = None

        header_btn.set_event_handler("click", toggle_accordion)

    def _populate_content_panel(self, content_panel, value, key):
        """Populate content panel based on value type"""
        if isinstance(value, str):
            value_row = self.create_table_row("Content", value)
            content_panel.add_component(value_row)
        elif isinstance(value, list) and value:
            self._add_list_items(content_panel, value, key)
        elif isinstance(value, dict):
            self._add_dict_items(content_panel, value)

    def _add_list_items(self, content_panel, items, section_key):
        """Add list items with radio buttons"""
        radio_group = []
        for idx, item in enumerate(items):
            item_panel = self.create_item_panel(item, section_key, idx, radio_group)
            if item_panel:
                content_panel.add_component(item_panel)
                content_panel.add_component(Spacer(height=5))

    def _add_dict_items(self, content_panel, data_dict):
        """Add dictionary items as table rows"""
        for dict_key, dict_value in data_dict.items():
            value_row = self.create_table_row(dict_key, dict_value)
            content_panel.add_component(value_row)

    def create_item_panel(self, item, section_key: str, index, radio_group):
        """Create a panel for a single item with radio button"""
        main_panel = self._create_item_container()
        header_section = self._create_item_header()
        radio = self._create_radio_button(section_key, index)

        self._setup_radio_selection(radio, main_panel, section_key, index, item)
        radio_group.append(radio)

        header_section.add_component(radio)
        main_panel.add_component(header_section)

        content_table = self._create_item_content(item)
        main_panel.add_component(content_table)

        return main_panel

    def _create_item_container(self):
        """Create main container for item"""
        return ColumnPanel(
            background="white",
            spacing_above="none",
            spacing_below="none",
            border="1px solid theme:Gray 700",
            role="elevated-card",
        )

    def _create_item_header(self):
        """Create header section for item"""
        return FlowPanel(
            align="left",
            spacing="medium",
            background="theme:Gray 50",
            spacing_above="none",
            spacing_below="none",
        )

    def _create_radio_button(self, section_key, index):
        """Create radio button for item selection"""
        option_number = index + 1
        return m3.RadioButton(
            value=f"{section_key}_{index}",
            group_name=section_key,
            text=f"{section_key.removesuffix('s').title()} #{option_number}",
            font_size=14,
            bold=True,
            spacing_above="none",
            spacing_below="none",
            spacing="small",
        )

    def _setup_radio_selection(self, radio, main_panel, section_key, index, item):
        """Setup radio button selection behavior"""

        def radio_changed(sender, **event_args):
            if sender.selected:
                self.selected_values[section_key] = {"index": index, "value": item}
                main_panel.background = "theme:Primary 50"
            else:
                main_panel.background = "white"

        radio.set_event_handler("x-change", radio_changed)

    def _create_item_content(self, item):
        """Create content display for item"""
        content_table = ColumnPanel(
            spacing_above="none",
            spacing_below="none",
            role="outlined-card",
            wrap_on="mobile",
        )

        if isinstance(item, dict):
            for field_key, field_value in item.items():
                field_row = self.create_table_row(field_key, field_value)
                content_table.add_component(field_row, full_width_row=True)
        else:
            field_row = self.create_table_row("Value", str(item))
            content_table.add_component(field_row)

        return content_table

    def create_table_row(self, field_key, field_value):
        """Create a table-like row with key and value columns"""
        row_container = FlowPanel(
            align="left",
            spacing_above="none",
            spacing_below="none",
            gap="tiny",
            role="outlined-card",
        )

        # Add components
        row_container.add_component(Spacer(), width="10px")

        key_label = self._create_key_label(field_key)
        row_container.add_component(key_label, width="5%")

        value_component = self._create_value_component(field_value)
        row_container.add_component(value_component, width="50%", expand=True)

        return row_container

    def _create_key_label(self, field_key):
        """Create formatted key label"""
        return Label(
            text=f"{self.format_title(field_key)}:",
            bold=True,
            font_size=13,
            foreground="theme:Primary 600",
            role="outlined-card",
        )

    def _create_value_component(self, field_value):
        """Create value component based on value type"""
        if isinstance(field_value, list):
            return self._create_list_value_component(field_value)
        else:
            return Label(text=str(field_value), font_size=13)

    def _create_list_value_component(self, field_value):
        """Create component for list values"""
        if all(isinstance(item, str) for item in field_value):
            # Simple string list
            value_text = ", ".join(field_value)
            return Label(
                text=value_text,
                font_size=13,
                role="outlined-card",
            )
        else:
            # Complex list
            value_component = ColumnPanel()
            for item in field_value:
                if isinstance(item, dict):
                    item_text = self.get_item_summary(item)
                    value_component.add_component(
                        Label(
                            text=f"• {item_text}",
                            font_size=12,
                            role="outlined-card",
                        )
                    )
                else:
                    value_component.add_component(
                        Label(text=f"• {str(item)}", font_size=12)
                    )
            return value_component

    def get_item_summary(self, item_dict):
        """Get a summary string for a dictionary item"""
        # Try to find the first available key that might be descriptive
        for key in item_dict.keys():
            if any(identifier in key.lower() for identifier in ['name', 'title', 'id', 'theme', 'type', 'task']):
                return str(item_dict[key])
        
        # Return first key-value pair if no descriptive field found
        if item_dict:
            first_key = list(item_dict.keys())[0]
            return f"{first_key}: {item_dict[first_key]}"
        
        return "Item"

    def create_dict_display(self, data_dict):
        """Create a formatted display for a dictionary using table-like layout"""
        panel = ColumnPanel(spacing_above="none")

        for key, value in data_dict.items():
            field_row = self.create_table_row(key, value)
            panel.add_component(field_row)

        return panel

    def format_title(self, text):
        """Format a key name into a readable title"""
        return text.replace("_", " ").title()

    def submit_selections(self, **event_args):
        """Handle submit button click - process selected values"""
        if not self.selected_values:
            alert("Please make at least one selection")
            return

        result = self._format_selection_result()
        alert(result, title="Selections Submitted")

    def _format_selection_result(self):
        """Format selected values for display"""
        result = "Selected Options:\n\n"
        for section, data in self.selected_values.items():
            result += f"{self.format_title(section)}:\n"
            result += f"  Index: {data['index']}\n"

            if isinstance(data["value"], dict):
                # Display all key-value pairs for selected items
                for key, value in data["value"].items():
                    result += f"  {self.format_title(key)}: {value}\n"
            result += "\n"

        return result

    def get_selected_values(self):
        """Get the currently selected values"""
        return self.selected_values

    def load_sample_data(self, **event_args):
        """Load and process sample data"""

    # Example usage - call this from your form's init or a button click
    def load_sample_data(self, **event_args):
        """
        Load and process sample data
        """
        # Your AI response data here
        sample_data = {
            "themes": [
                {
                    "theme": "Anfield Atmosphere",
                    "description": "Bring the spirit of Anfield home with red and white decorations, banners, and vintage football memorabilia. Create a mini-hall of fame with iconic moments from Liverpool's history.",
                    "colors": "Liverpool Red, White, and Black",
                    "decorIdeas": [
                        "Bunting with Liverpool motifs",
                        "Photo wall of legendary moments",
                        "Football-shaped balloons",
                    ],
                },
                {
                    "theme": "Modern Fan Zone",
                    "description": "A sleek, contemporary design that uses LED lighting, dynamic visuals, and interactive displays. Perfect for a season opener party.",
                    "colors": "Red, Metallic Silver, and Black",
                    "decorIdeas": [
                        "LED strips in key areas",
                        "Digital photo booth with Liverpool filters",
                        "Modern table centerpieces with mini footballs",
                    ],
                },
                {
                    "theme": "Retro Football Fiesta",
                    "description": "A nostalgic tribute to football's golden eras with vintage posters, retro props, and classic tunes. Emphasize fun, games, and conversation.",
                    "colors": "Deep Red, Cream, and Navy Blue",
                    "decorIdeas": [
                        "Retro vinyl records playing classic sports anthems",
                        "Vintage football jerseys on the walls",
                        "Old-school pennants and scarves",
                    ],
                },
            ],
            "menus": [
                {
                    "type": "British Pub Fare",
                    "description": "Classic pub-inspired snacks and finger foods that keep the party spirit alive. Think hearty, shareable dishes with a twist.",
                    "options": [
                        "Mini fish and chips in cones",
                        "Scotch eggs",
                        "Pub-style sliders",
                        "Loaded fries",
                    ],
                    "beverageSuggestions": [
                        "Craft beers",
                        "Cider",
                        "Non-alcoholic ginger beer",
                    ],
                    "budgetAllocation": "Approximately 50% of the total budget",
                },
                {
                    "type": "Gourmet Game Day",
                    "description": "Elevate the typical game day experience with gourmet twists on traditional favorites. Focus on quality, presentation, and shareable plates.",
                    "options": [
                        "Gourmet mini burgers",
                        "Truffle fries",
                        "Artisan pizzas cut into bite-sized pieces",
                        "Exotic dips with artisan bread",
                    ],
                    "beverageSuggestions": [
                        "Specialty cocktails with a red twist",
                        "Mocktails",
                        "Premium soft drinks",
                    ],
                    "budgetAllocation": "Approximately 60% of the total budget including some premium ingredients",
                },
                {
                    "type": "Interactive Snack Stations",
                    "description": "Set up self-serve stations that allow guests to customize their food. The fun of building your own dish adds to the interactive vibe.",
                    "options": [
                        "DIY nacho bar with assorted toppings",
                        "Build-your-own slider station",
                        "Custom hot dog stand with varied condiments",
                    ],
                    "beverageSuggestions": [
                        "Soda bar with mix-in options",
                        "Infused water",
                    ],
                    "budgetAllocation": "Approximately 45% of the total budget",
                },
            ],
            "tasks": [
                {
                    "task": "Decorations and Setup",
                    "details": "Purchase or gather Liverpool-themed decorations, banners, and props; set up the space with designated photo zones and seating areas.",
                    "duration": "3-4 hours",
                    "due_date": "2025-08-20",
                },
                {
                    "task": "Menu Planning and Food Prep",
                    "details": "Finalize the menu, confirm ingredients, prepare or coordinate any pre-cooked items, and set up snack stations or serving areas.",
                    "duration": "2-3 hours",
                    "due_date": "2025-08-20",
                },
                {
                    "task": "Audio/Visual Setup",
                    "details": "Set up the viewing area with proper lighting, sound systems, and test streaming the game to ensure a seamless viewing experience.",
                    "duration": "1-2 hours",
                    "due_date": "2025-08-20",
                },
                {
                    "task": "Icebreakers and Game Setup",
                    "details": "Plan and gather materials for interactive games and icebreaker activities. Set up any required equipment or props.",
                    "duration": "1 hour",
                    "due_date": "2025-08-20",
                },
            ],
            "budget_tracker": [
                {
                    "category": "Decorations",
                    "suggested_amount": 150,
                    "notes": "Allocate funds to purchase or rent Liverpool-themed decor items, including banners, balloons, and photo props.",
                },
                {
                    "category": "Food and Beverages",
                    "suggested_amount": 300,
                    "notes": "This covers ingredients, possibly pre-made food items, beverages, and any extra serving supplies. Adjust based on menu choice.",
                },
                {
                    "category": "Audio/Visual Equipment",
                    "suggested_amount": 100,
                    "notes": "If additional equipment such as a projector or speakers are needed, these funds should cover any rental fees.",
                },
                {
                    "category": "Miscellaneous & Games",
                    "suggested_amount": 50,
                    "notes": "For icebreaker props, small awards for game winners, or any last-minute supplies.",
                },
            ],
            "icebreakers": [
                {
                    "name": "Liverpool Trivia Challenge",
                    "details": "Prepare a set of trivia questions revolving around Liverpool's history, players, and memorable games. Divide guests into teams and award small prizes for winners.",
                },
                {
                    "name": "Football Bingo",
                    "details": "Create bingo cards with common match events (e.g., a corner, a foul, a goal celebration). As the game progresses, guests mark their cards.",
                },
                {
                    "name": "Fan Stories Sharing",
                    "details": "Encourage guests to share their favorite Liverpool memory or game experience. This can be a round-robin where everyone gets to speak briefly.",
                },
            ],
            "games": [
                {
                    "name": "Mini Indoor Penalty Shootout",
                    "details": "Set up a small goal (or target area) in a hallway or open space and have guests take turns trying to score using a soft football.",
                },
                {
                    "name": "Football Pictionary",
                    "details": "Prepare a list of football-related terms and have guests draw them within a time limit while their team guesses the term.",
                },
                {
                    "name": "Score Prediction Game",
                    "details": "Before the match starts, have guests predict the final score. Award a fun prize to the person whose prediction is the closest.",
                },
            ],
            "recommendations": [
                "Ensure you test your streaming and sound systems well in advance to avoid any technical difficulties during the game.",
                "Consider creating a themed invitation e-card in Liverpool colors to build excitement among attendees.",
                "Prepare a backup plan for any potential weather or technical issues, even though it's an indoor event.",
                "Set up a dedicated area for a short 'pre-game' discussion or analysis, encouraging fans to share their predictions and insights.",
                "Use social media or a group chat to share updates, photos, and memorable moments during the event to enhance engagement.",
            ],
        }
        return sample_data
        # self.process_json_response(sample_data)
        # Any code you write here will run before the form opens.

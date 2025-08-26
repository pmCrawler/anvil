from ._anvil_designer import AIResponseTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json


class AIResponse(AIResponseTemplate):
    def __init__(self, resp=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Store selected values for each section
        self.selected_values = {}

        # self.ai_response = anvil.server.call("get_ai_response")
        self.ai_response = (
            properties if resp is None else resp
        )  # properties  # self.load_sample_data()
        self.process_json_response(self.ai_response)

    def process_json_response(self, json_response):
        """
        Main function to process JSON response and create dynamic controls

        Args:
            json_response: The JSON response from AI (can be dict or string)
        """
        # Clear existing components
        self.cpanel_ai_resp.clear()
        self.selected_values = {}

        # Parse JSON if it's a string
        if isinstance(json_response, str):
            try:
                json_data = json.loads(json_response)
            except json.JSONDecodeError:
                alert("Invalid JSON format")
                return
        else:
            json_data = json_response

        # If the response is a list with one item, extract it
        if isinstance(json_data, list) and len(json_data) > 0:
            json_data = json_data[0]

        # Create main container for all accordions
        main_container = ColumnPanel()

        # Process each root element
        for key, value in json_data.items():
            # Create accordion for this root element
            accordion_panel = self.create_accordion_section(key, value)
            if accordion_panel:
                main_container.add_component(accordion_panel)

        # Add the main container to the form
        self.cpanel_ai_resp.add_component(main_container)

        # # Add a submit button at the bottom
        # submit_btn = m3.Button(
        #     text="Save",
        #     appearance="filled",
        # )
        # submit_btn.set_event_handler("click", self.submit_selections)
        # self.cpanel_ai_resp.add_component(submit_btn)

    def create_accordion_section(self, key, value):
        """Create an accordion section for a root element"""

        # Create the accordion container
        accordion = ColumnPanel(
            spacing_above="none",
            spacing_below="none",
            wrap_on="mobile",
        )

        # Create expandable card
        card = m3.Card(appearance="outlined", visible=False)

        # Create content panel (initially hidden)
        cpanel_ai_resp = ColumnPanel(
            visible=False,
            spacing_above="none",
            wrap_on="mobile",
        )

        # Track expanded state
        is_expanded = {"value": False}

        # Create header container
        # header_container = ColumnPanel()
        header_container = m3.Text(
            scale="small",
        )

        # Use Button with custom styling for the accordion header
        header_btn = m3.Button(
            text=f"▶ {self.format_title(key)}",
            align="left",
            icon_align="left",
            appearance="tonal",
        )

        def toggle_accordion(**event_args):
            """Toggle accordion expansion"""
            is_expanded["value"] = not is_expanded["value"]
            cpanel_ai_resp.visible = is_expanded["value"]
            card.visible = is_expanded["value"]

            # Update arrow direction and background
            arrow = "▼" if is_expanded["value"] else "▶"
            header_btn.text = f"{arrow} {self.format_title(key)}"

            # Change background to indicate state
            if is_expanded["value"]:
                header_btn.background = "theme:Primary 100"
                header_btn.role = "filled-button"
            else:
                header_btn.background = "theme:Gray 50"
                header_btn.role = None

        # Set event handler for click only
        header_btn.set_event_handler("click", toggle_accordion)
        header_container.add_component(header_btn)

        # Process the value based on its type
        if isinstance(value, str):
            # Simple string value - also use table format for consistency
            value_row = self.create_table_row("Content", value)
            cpanel_ai_resp.add_component(value_row)

        elif isinstance(value, list):
            # List of items - create radio buttons for selection
            if len(value) > 0:
                # Initialize RadioButton group for this section
                radio_group = []

                for idx, item in enumerate(value):
                    item_panel = self.create_item_panel(item, key, idx, radio_group)
                    if item_panel:
                        cpanel_ai_resp.add_component(item_panel)
                        cpanel_ai_resp.add_component(Spacer(height=5))

        elif isinstance(value, dict):
            # Single dictionary - display as formatted table
            for dict_key, dict_value in value.items():
                value_row = self.create_table_row(dict_key, dict_value)
                cpanel_ai_resp.add_component(value_row)

        # Assemble the card
        # card_content = ColumnPanel()
        card_content = m3.CardContentContainer(margin="16px")
        # card_content.add_component(header_container)
        card_content.add_component(cpanel_ai_resp)
        # card.add_component(header_container)
        card.add_component(card_content)

        accordion.add_component(header_container, full_width_row=True)
        accordion.add_component(card)

        return accordion

    def create_item_panel(self, item, section_key: str, index, radio_group):
        """
        Create a panel for a single item with radio button

        Args:
            item: The item data (usually a dict)
            section_key: The parent section key
            index: The index of this item
            radio_group: List to track radio buttons in this group

        Returns:
            An Anvil panel component
        """
        # Main container for the item
        main_panel = ColumnPanel(
            background="white",
            spacing_above="none",
            spacing_below="none",
            border="1px solid theme:Gray 700",
            role="elevated-card",
        )

        # Create a header section with radio button
        header_section = FlowPanel(
            align="left",
            spacing="medium",
            background="theme:Gray 50",
            spacing_above="none",
            spacing_below="none",
        )

        # Create radio button with a label
        option_number = index + 1
        radio = m3.RadioButton(
            value=f"{section_key}_{index}",
            group_name=section_key,
            # text=f"Option {option_number}",
            text=f"{section_key.removesuffix('s').title()} #{option_number}",
            font_size=14,
            bold=True,
            spacing_above="none",
            spacing_below="none",
            spacing="small",
        )

        # Add change handler
        def radio_changed(sender, **event_args):
            if sender.selected:
                self.selected_values[section_key] = {"index": index, "value": item}
                # Highlight selected panel
                main_panel.background = "theme:Primary 50"
            else:
                main_panel.background = "white"

        radio.set_event_handler("x-change", radio_changed)
        radio_group.append(radio)

        # Add radio button to header
        header_section.add_component(radio)
        main_panel.add_component(header_section)

        # Create content table (table-like layout without borders)
        content_table = ColumnPanel(
            spacing_above="none",
            spacing_below="none",
            # border="1px solid #d1d2d4",
            role="outlined-card",
            wrap_on="mobile",
        )

        if isinstance(item, dict):
            # Display dictionary fields in table format
            for field_key, field_value in item.items():
                field_row = self.create_table_row(field_key, field_value)
                content_table.add_component(field_row, full_width_row=True)
        else:
            # Display as simple text in a single row
            field_row = self.create_table_row("Value", str(item))
            content_table.add_component(field_row)

        main_panel.add_component(content_table)

        return main_panel

    def create_table_row(self, field_key, field_value):
        """
        Create a table-like row with key and value columns

        Args:
            field_key: The field name (left column)
            field_value: The field value (right column)

        Returns:
            An Anvil component representing a table row
        """
        # Create container with indentation
        row_container = FlowPanel(
            align="left",
            spacing_above="none",
            spacing_below="none",
            # width="100%",
            gap="tiny",
            role="outlined-card",
        )

        # Add indentation spacer
        # [H.E. 8/21/25] - added "width" arg to add_component
        row_container.add_component(Spacer(), width="10px")

        # Key column with fixed width
        key_label = Label(
            text=f"{self.format_title(field_key)}:",
            bold=True,
            font_size=13,
            foreground="theme:Primary 600",
            # width="120px",  # Fixed width to prevent wrapping
            # Fixed width to prevent wrapping
            role="outlined-card",
        )
        # [H.E. 8/21/25] - added "width" arg to add_component
        row_container.add_component(key_label, width="5%")

        # Value column
        if isinstance(field_value, list):
            # Handle list values
            if all(isinstance(item, str) for item in field_value):
                # Simple string list - display as comma-separated
                value_text = ", ".join(field_value)
                value_component = Label(
                    text=value_text,
                    font_size=13,
                    role="outlined-card",
                )
            else:
                # Complex list - create nested display
                value_component = ColumnPanel()
                for item in field_value:
                    if isinstance(item, dict):
                        # For complex nested items, show key fields only
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
                            Label(text=f"• {str(item)}", font_size=12),
                        )
        else:
            # Simple value - let it flow naturally without width restriction
            value_component = Label(text=str(field_value), font_size=13)

        # [H.E. 8/21/25] - added "width" arg to add_component
        row_container.add_component(value_component, width="50%", expand=True)

        return row_container

    def get_item_summary(self, item_dict):
        """
        Get a summary string for a dictionary item

        Args:
            item_dict: Dictionary to summarize

        Returns:
            Summary string
        """
        # Look for common identifier fields
        for key in ["name", "title", "id", "theme", "menu_option"]:
            if key in item_dict:
                return str(item_dict[key])

        # If no identifier found, return first value
        if item_dict:
            first_key = list(item_dict.keys())[0]
            return f"{first_key}: {item_dict[first_key]}"

        return "Item"

    def create_dict_display(self, data_dict):
        """
        Create a formatted display for a dictionary using table-like layout

        Args:
            data_dict: Dictionary to display

        Returns:
            An Anvil component
        """
        panel = ColumnPanel(spacing_above="none")

        for key, value in data_dict.items():
            field_row = self.create_table_row(key, value)
            panel.add_component(field_row)

        return panel

    def format_title(self, text):
        """
        Format a key name into a readable title

        Args:
            text: The original text

        Returns:
            Formatted title string
        """
        # Replace underscores with spaces and capitalize words
        return text.replace("_", " ").title()

    def submit_selections(self, **event_args):
        """
        Handle submit button click - process selected values
        """
        if not self.selected_values:
            alert("Please make at least one selection")
            return

        # Process the selected values
        result = "Selected Options:\n\n"
        for section, data in self.selected_values.items():
            result += f"{self.format_title(section)}:\n"
            result += f"  Index: {data['index']}\n"

            # Display key details from the selected item
            if isinstance(data["value"], dict):
                for key, value in data["value"].items():
                    if key in ["name", "theme", "menu_option", "task", "item"]:
                        result += f"  {self.format_title(key)}: {value}\n"
            result += "\n"

        # You can replace this with your own processing logic
        alert(result, title="Selections Submitted")

        # Call server function if needed
        # anvil.server.call('process_selections', self.selected_values)

    def get_selected_values(self):
        """
        Get the currently selected values

        Returns:
            Dictionary of selected values by section
        """
        return self.selected_values

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

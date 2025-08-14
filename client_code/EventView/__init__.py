from ._anvil_designer import EventViewTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json


class EventView(EventViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Store selected values for each section
        self.selected_values = {}
        self.ai_response = anvil.server.call("get_ai_response")
        self.process_json_response(self.ai_response)

    def process_json_response(self, json_response):
        """
        Main function to process JSON response and create dynamic controls

        Args:
            json_response: The JSON response from AI (can be dict or string)
        """
        # Clear existing components
        self.content_panel.clear()
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
        self.content_panel.add_component(main_container)

        # Add a submit button at the bottom
        submit_btn = Button(text="Submit Selections", role="primary-color")
        submit_btn.set_event_handler("click", self.submit_selections)
        self.content_panel.add_component(submit_btn)

    def create_accordion_section(self, key, value):
        """
        Create an accordion section for a root element

        Args:
            key: The name of the root element
            value: The value (can be string, dict, or list)

        Returns:
            An Anvil component containing the accordion
        """
        # Create the accordion container
        accordion = ColumnPanel(spacing_above="none", spacing_below="none")

        # Create expandable card
        card = m3.Card()
        card.role = "elevated-card"

        # Create content panel (initially hidden)
        content_panel = ColumnPanel(
            visible=False,
            spacing_above="none",
            wrap_on="mobile",
        )

        # Track expanded state
        is_expanded = {"value": False}

        # Create header container
        header_container = ColumnPanel()

        # Use Button with custom styling for the accordion header
        header_btn = m3.Button(
            text=f"▶ {self.format_title(key)}",
            font_size=14,
            bold=True,
            background="theme:Gray 50",
            foreground="theme:Primary 700",
            align="left",
            icon_align="left",
        )

        def toggle_accordion(**event_args):
            """Toggle accordion expansion"""
            is_expanded["value"] = not is_expanded["value"]
            content_panel.visible = is_expanded["value"]

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
            content_panel.add_component(value_row)

        elif isinstance(value, list):
            # List of items - create radio buttons for selection
            if len(value) > 0:
                # Initialize RadioButton group for this section
                radio_group = []

                for idx, item in enumerate(value):
                    item_panel = self.create_item_panel(item, key, idx, radio_group)
                    if item_panel:
                        content_panel.add_component(item_panel)
                        content_panel.add_component(Spacer(height=5))

        elif isinstance(value, dict):
            # Single dictionary - display as formatted table
            for dict_key, dict_value in value.items():
                value_row = self.create_table_row(dict_key, dict_value)
                content_panel.add_component(value_row)

        # Assemble the card
        card_content = ColumnPanel()
        card_content.add_component(header_container)
        card_content.add_component(content_panel)
        card.add_component(card_content)

        accordion.add_component(card)

        return accordion

    def create_item_panel(self, item, section_key, index, radio_group):
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
            text=f"Option {option_number}",
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
        # content_table = LinearPanel(
        #     spacing_above="none",
        #     spacing_below="none",
        #     border="0.5px solid #d1d2d4",
        # )

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
            # spacing="none",
            spacing_above="none",
            spacing_below="none",
            width="100%",
            gap="none",
            role="outlined-card",
        )

        # Add indentation spacer
        row_container.add_component(Spacer(width="30px"))

        # Key column with fixed width
        key_label = Label(
            text=f"{self.format_title(field_key)}:",
            bold=True,
            font_size=13,
            foreground="theme:Primary 600",
            width="120px",  # Fixed width to prevent wrapping
            role="outlined-card",
        )
        row_container.add_component(key_label)

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
                            Label(text=f"• {str(item)}", font_size=12)
                        )
        else:
            # Simple value - let it flow naturally without width restriction
            value_component = Label(text=str(field_value), font_size=13)

        row_container.add_component(value_component)

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
            "budget": "Assume a moderate budget with cost-saving DIY elements where possible",
            "themes": [
                {
                    "theme": "Floral Garden Party",
                    "description": "Soft pastels and floral accents to celebrate the impending arrival in a spring setting.",
                    "colors": "Light pink, mint green, and lavender",
                    "decorations": "Fresh flowers, DIY paper garlands, pastel-colored balloons, fabric bunting, potted plants for table centerpieces",
                    "notes": "Perfect for spring; indoor club house can be easily transformed with these accents.",
                },
                {
                    "theme": "Vintage Parisian Chic",
                    "description": "Inspired by old-world charm with hints of romance and elegance for a baby girl shower.",
                    "colors": "Blush pink, cream, gold accents",
                    "decorations": "Antique styled frames, lace table runners, string lights, delicate teacups as centerpieces, soft classical music",
                    "notes": "This theme adds a nostalgic twist and is adaptable to an indoor setting.",
                },
            ],
            "menus": [
                {
                    "menu_option": "Mediterranean-Inspired Buffet",
                    "description": "A selection of dishes inspired by Greek, Italian, and Middle Eastern cuisines.",
                    "dishes": [
                        "Falafel wraps with tzatziki sauce",
                        "Grilled chicken shawarma sliders",
                    ],
                }
            ],
        }

        self.process_json_response(sample_data)

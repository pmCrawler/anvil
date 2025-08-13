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

        # Sample JSON data (you can replace this with your actual data source)
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
        accordion = ColumnPanel(spacing_above="small", spacing_below="small")

        # Create expandable card
        card = m3.Card()
        card.role = "elevated-card"

        # Create content panel (initially hidden)
        content_panel = ColumnPanel(visible=False, spacing_above="small")

        # Track expanded state
        is_expanded = {"value": False}

        # Create header container
        header_container = ColumnPanel()

        # Use Button with custom styling for the accordion header
        header_btn = Button(
            text=f"▶ {self.format_title(key)}",
            font_size=16,
            bold=True,
            background="theme:Gray 50",
            foreground="theme:Primary 700",
            align="full",
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
            # Simple string value - display as label
            content_panel.add_component(Label(text=value, font_size=14))

        elif isinstance(value, list):
            # List of items - create radio buttons for selection
            if len(value) > 0:
                # Initialize RadioButton group for this section
                radio_group = []

                for idx, item in enumerate(value):
                    item_panel = self.create_item_panel(item, key, idx, radio_group)
                    if item_panel:
                        content_panel.add_component(item_panel)
                        content_panel.add_component(Spacer(height=10))

        elif isinstance(value, dict):
            # Single dictionary - display as formatted content
            item_panel = self.create_dict_display(value)
            content_panel.add_component(item_panel)

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
        panel = ColumnPanel(
            background="theme:Gray 100", spacing_above="small", spacing_below="small"
        )

        # Create horizontal panel for radio button and content
        row_panel = FlowPanel(align="left", spacing="medium")

        # Create radio button
        radio = RadioButton(
            value=f"{section_key}_{index}",
            group_name=section_key,
            spacing_above="small",
        )

        # Add change handler
        def radio_changed(sender, **event_args):
            if sender.selected:
                self.selected_values[section_key] = {"index": index, "value": item}

        radio.set_event_handler("change", radio_changed)
        radio_group.append(radio)

        # Create content panel
        content = ColumnPanel()

        if isinstance(item, dict):
            # Display dictionary fields
            for field_key, field_value in item.items():
                field_panel = self.create_field_display(field_key, field_value)
                content.add_component(field_panel)
        else:
            # Display as simple text
            content.add_component(Label(text=str(item)))

        row_panel.add_component(radio)
        row_panel.add_component(content)
        panel.add_component(row_panel)

        return panel

    def create_field_display(self, field_key, field_value):
        """
        Create a display for a single field

        Args:
            field_key: The field name
            field_value: The field value

        Returns:
            An Anvil component
        """
        field_panel = FlowPanel(align="left", spacing="small")

        # Format the field name
        label = Label(
            text=f"{self.format_title(field_key)}:",
            bold=True,
            font_size=13,
            foreground="theme:Primary 500",
        )

        # Handle different value types
        if isinstance(field_value, list):
            # For lists, create a formatted string or sub-components
            if all(isinstance(item, str) for item in field_value):
                # Simple string list
                value_text = ", ".join(field_value)
                value_label = Label(text=value_text, font_size=13)
                field_panel.add_component(label)
                field_panel.add_component(value_label)
            else:
                # Complex list - create vertical layout
                vert_panel = ColumnPanel()
                vert_panel.add_component(label)
                for item in field_value:
                    if isinstance(item, dict):
                        sub_panel = self.create_dict_display(item)
                        vert_panel.add_component(sub_panel)
                    else:
                        vert_panel.add_component(
                            Label(text=f"  • {str(item)}", font_size=12)
                        )
                return vert_panel
        else:
            # Simple value
            value_label = Label(text=str(field_value), font_size=13)
            field_panel.add_component(label)
            field_panel.add_component(value_label)

        return field_panel

    def create_dict_display(self, data_dict):
        """
        Create a formatted display for a dictionary

        Args:
            data_dict: Dictionary to display

        Returns:
            An Anvil component
        """
        panel = ColumnPanel(spacing_above="small")

        for key, value in data_dict.items():
            field_display = self.create_field_display(key, value)
            panel.add_component(field_display)

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

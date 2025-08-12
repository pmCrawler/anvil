import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def get_ai_response(): 
    response = {
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
            {
                "theme": "Modern Minimalist",
                "description": "A chic and elegant design that uses geometric shapes and subtle colors to celebrate new life.",
                "colors": "Soft blush, white, and gray accents",
                "decorations": "Simple balloon installations with metallic touches, minimalist floral arrangements, clean-lined table settings, modern art prints",
                "notes": "Great for a contemporary vibe with less clutter but high impact.",
            },
            {
                "theme": "Fairytale Enchantment",
                "description": "Create a dreamy, storybook atmosphere with whimsical elements to celebrate the little princess.",
                "colors": "Pastel pink, light blue, white with silver sparkles",
                "decorations": "DIY paper castles, fairy lights, tulle and lace drapes, themed centerpieces like mini crowns or magic wands",
                "notes": "An enchanting theme that pairs well with indoor lighting and budget-friendly DIY decor.",
            },
        ],
        "menus": [
            {
                "menu_option": "Mediterranean-Inspired Buffet",
                "description": "A selection of dishes inspired by Greek, Italian, and Middle Eastern cuisines with vegetarian and non-vegetarian options.",
                "dishes": [
                    "Falafel wraps with tzatziki sauce",
                    "Grilled chicken shawarma sliders",
                    "Greek salad with olives and feta",
                    "Tabbouleh and hummus platter",
                    "Mini spanakopita and stuffed grape leaves",
                ],
                "notes": "Ensure some gluten-free options are available. Incorporate fresh breads and a variety of dips to please diverse palates.",
            },
            {
                "menu_option": "Asian Fusion Delights",
                "description": "Mixing flavors from Japanese, Chinese, and Thai cuisines to create an eclectic yet balanced menu.",
                "dishes": [
                    "Vegetable and shrimp tempura",
                    "Chicken satay with peanut sauce",
                    "Thai green papaya salad (a lighter twist)",
                    "Steamed bao buns with various fillings (including tofu for vegetarians)",
                    "Assorted sushi rolls with a focus on light flavors",
                ],
                "notes": "Ensure soy sauce alternatives (like tamari) are available for gluten-free guests and have options labeled for common allergens.",
            },
            {
                "menu_option": "Latin American Fiesta",
                "description": "A vibrant menu featuring dishes from Mexico, Peru, and Brazil with fresh flavors and colorful presentation.",
                "dishes": [
                    "Mini taco stations with assorted fillings",
                    "Ceviche (with fish and a vegetarian version with hearts of palm)",
                    "Arepas with a variety of toppings",
                    "Quinoa salad with black beans and corn",
                    "Fresh fruit skewers with a light chili-lime dressing",
                ],
                "notes": "Include vegetarian and dairy-free options where needed. Consider offering a fusion of traditional and contemporary dishes.",
            },
        ],
        "tasks": [
            {
                "task": "Book Club House Venue",
                "description": "Ensure the indoor club house is reserved for the date and time of the event.",
                "duration": "1 hour",
                "due_date": "2026-02-15",
            },
            {
                "task": "Confirm Catering Service",
                "description": "Finalize the menu choices and communicate any dietary restrictions to the caterers.",
                "duration": "2 hours",
                "due_date": "2026-03-01",
            },
            {
                "task": "Purchase Decorations and DIY Supplies",
                "description": "Buy or gather supplies for your chosen theme decorations including balloons, fabrics, and floral arrangements.",
                "duration": "3 hours",
                "due_date": "2026-03-10",
            },
            {
                "task": "Plan Ice-breakers and Games",
                "description": "Prepare a list of interactive activities for guests and procure any necessary supplies or prizes.",
                "duration": "2 hours",
                "due_date": "2026-03-20",
            },
            {
                "task": "Setup Food and Beverage Stations",
                "description": "Coordinate with the caterer for effective food display and beverage setups.",
                "duration": "2 hours",
                "due_date": "2026-04-04",
            },
        ],
        "budget_tracker": [
            {
                "item": "Decorations",
                "allocated": "$300",
                "notes": "Use DIY elements and cost-effective supplies.",
            },
            {
                "item": "Food and Beverage",
                "allocated": "$1200",
                "notes": "Budget to cover multiple cuisine options and dietary requirements.",
            },
            {
                "item": "Venue",
                "allocated": "$200",
                "notes": "Estimated cost for club house rental if applicable.",
            },
            {
                "item": "Miscellaneous (Games, Prizes, Supplies)",
                "allocated": "$150",
                "notes": "For additional items like game supplies, prizes, and printed materials.",
            },
        ],
        "icebreakers": [
            {
                "name": "Baby Name Guesser",
                "description": "Guests suggest names or guess the baby’s name based on hints provided by the host. It sparks conversation and fun discussions.",
            },
            {
                "name": "Memory Lane",
                "description": "Guests share funny or touching baby-related stories or a childhood memory related to a similar event.",
            },
            {
                "name": "Two Truths and a Baby Lie",
                "description": "A baby-themed twist on the classic game where guests share two truths and one made-up fact relating to parenting or childhood memories.",
            },
        ],
        "games": [
            {
                "name": "Diaper Raffle",
                "description": "Guests bring a pack of diapers for entry into a raffle. Winners get fun prizes. It’s interactive and helps stock up for the baby.",
            },
            {
                "name": "Baby Bingo",
                "description": "Customized bingo cards featuring baby-related items or events. It’s a great way to engage everyone while waiting for a special moment.",
            },
            {
                "name": "Guess the Baby Food",
                "description": "Blindfolded participants sample different baby foods and guess the flavors. This game promises laughter and fun.",
            },
        ],
        "recommendations": [
            {
                "recommendation": "Photo Booth Setup",
                "description": "Create a designated photo area with themed props (e.g., baby bottles, mini crowns, floral frames) so guests can capture the memories.",
            },
            {
                "recommendation": "Guest Book with a Twist",
                "description": "Instead of a traditional guest book, have a station where guests write down parenting tips or wishes for the baby on cards that can later be assembled into a keepsake.",
            },
            {
                "recommendation": "Cultural Touchpoints",
                "description": "Incorporate small details from the menus into the decor – for example, themed table cards describing each cuisine's significance or a display of multicultural baby symbols.",
            },
            {
                "recommendation": "Customized Favors",
                "description": "Prepare small favor bags that reflect the event’s multicultural vibe – such as mini succulents, handmade soaps, or themed candies.",
            },
        ],
    }
    return response

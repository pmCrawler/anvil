import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

ai_response = [
    {
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
                "description": "Incorporate small options from the menus into the decor – for example, themed table cards describing each cuisine's significance or a display of multicultural baby symbols.",
            },
            {
                "recommendation": "Customized Favors",
                "description": "Prepare small favor bags that reflect the event’s multicultural vibe – such as mini succulents, handmade soaps, or themed candies.",
            },
        ],
    }
]

ai_response_2 = [
    {
        "themes": [
            {
                "name": "Tropical Escape",
                "description": "Bring a vacation vibe to your event with vibrant colors, palm leaves, tiki torches, and island music. This theme works great for outdoor events or for an indoor venue transformed with creative lighting and decor.",
            },
            {
                "name": "Retro 80s Party",
                "description": "Set the stage with neon colors, disco balls, and era-specific music. Encourage guests to dress in their best 1980s attire, and use arcade and retro gaming elements throughout the venue.",
            },
            {
                "name": "Enchanted Garden",
                "description": "Transform the venue into a whimsical garden with fairy lights, floral arrangements, and rustic table settings. This theme works excellently for daytime outdoor events but can be adapted for indoor spaces with creative lighting.",
            },
            {
                "name": "Modern Minimalistic Chic",
                "description": "Focus on sleek lines, a monochrome palette with bold accent colors, and elegant decor. This theme suits events where a sophisticated atmosphere is desired, and pooling together minimal art pieces can get a high-end feel.",
            },
        ],
        "menu": [
            {
                "approach": "Design an adaptable menu that fits within the budget, suits the event duration (e.g., 4-6 hours), and caters to a maximum number of attendees. Consider offering a mix of finger foods, small plates, and streamed stations to minimize waste and maximize enjoyment."
            },
            {
                "appetizers": [
                    {"option": "Seasonal Vegetable Crudités with assorted dips"},
                    {"option": "Mini Caprese Skewers drizzled with balsamic glaze"},
                    {
                        "option": "Gourmet Sliders (beef, vegetarian, or chicken options)"
                    },
                ]
            },
            {
                "main_courses": [
                    "Build-your-own taco or wrap station with diverse proteins and toppings",
                    "Pasta bar featuring two or three sauce choices with a vegetarian-friendly option",
                    "Customizable grain bowls with varying proteins, veggies, and dressings",
                ]
            },
            {
                "sides": [
                    "Mixed greens salad with a selection of dressings",
                    "Roasted seasonal vegetables",
                    "Gourmet flatbreads or artisanal breads accompanied by flavored butters",
                ]
            },
            {
                "desserts": [
                    "Mini pastries or cupcakes aligned with the event theme",
                    "Fruit skewers or a dessert station with bite-sized sweets",
                    "A themed cake or dessert centerpiece for a memorable reveal",
                ]
            },
            {
                "beverages": [
                    "Signature cocktails/mocktails themed to the event (e.g., Tropical Punch for a Tropical Escape)",
                    "A curated selection of wines and craft beers",
                    "Infused waters and specialty coffee/tea stations",
                ]
            },
        ],
        "place_settings": [
            {
                "option": "Customized Table Numbers",
                "description": "Integrate table numbers that match the event theme—such as small tropical shells for a Tropical Escape or neon signage for a Retro 80s Party.",
            },
            {
                "option": "Themed Centerpieces",
                "description": "Use floral arrangements, candles, or small decor items that tie into the theme. For example, an Enchanted Garden might feature mason jars filled with wildflowers.",
            },
            {
                "option": "Coordinated Tableware",
                "description": "Select plates, napkins, and cutlery that follow the color scheme and style of the event. Minimalistic events might use white or metallic accents while retro themes could incorporate bold, patterned designs.",
            },
            {
                "option": "Personalized Place Cards",
                "description": "Offer guests a personalized card with a tip or fun fact related to the theme, creating a memorable and interactive element from the moment they are seated.",
            },
        ],
        "gift_bags": {
            "considerations": "Align gift bag contents with the event theme and budget while ensuring that the items are useful and memorable for guests.",
            "ideas": [
                {
                    "theme": "Tropical Escape",
                    "contents": [
                        "Mini bottle of sunscreen or after-sun lotion",
                        "Customized sunglasses",
                        "Local tropical-flavored snacks (e.g., coconut cookies)",
                        "A small plant or succulent in a themed pot",
                    ],
                },
                {
                    "theme": "Retro 80s Party",
                    "contents": [
                        "Retro-themed keychain or mini Rubik's Cube",
                        "Cassette or CD of iconic 80s hits (or a custom playlist card)",
                        "Neon-colored accessories (e.g., wristbands or small sunglasses)",
                        "Vintage-style candy or treats from the era",
                    ],
                },
                {
                    "theme": "Enchanted Garden",
                    "contents": [
                        "Seed packets for native flowers or herbs",
                        "Miniature terrarium or a small potted plant",
                        "Handmade soap or a scented candle inspired by nature",
                        "Artisan tea bags or a specialty herbal blend",
                    ],
                },
                {
                    "theme": "Modern Minimalistic Chic",
                    "contents": [
                        "Elegant stationery set or a high-quality notebook",
                        "Sleek keychain or minimalist jewelry",
                        "Gourmet chocolates with simple, modern packaging",
                        "A small voucher for a local coffee shop or boutique",
                    ],
                },
            ],
        },
        "activities": {
            "overview": "Plan a schedule that balances structured group activities, free networking, and enough downtime to appreciate the food and decor. The following suggestions include ideas on the activity types, durations, and timing to create a well-rounded experience.",
            "activity_schedule": [
                {
                    "time": "0:00 - 0:30",
                    "activity": "Welcome Reception",
                    "description": "Greet guests with signature drinks and light appetizers. Consider using a themed welcome video or interactive ice-breakers related to the event theme.",
                },
                {
                    "time": "0:30 - 1:30",
                    "activity": "Interactive Activity/Group Games",
                    "description": "Design group activities that fit the theme. For instance, a Tropical Escape event could include a limbo contest or hula hoop competition; a Retro 80s Party might have a dance-off or arcade game challenge. Ensure each activity is 15-20 minutes long with a few rounds.",
                },
                {
                    "time": "1:30 - 2:30",
                    "activity": "Themed Workshop or Demonstration",
                    "description": "Incorporate an engaging session like a cocktail-making demonstration for Tropical themes, a DIY craft station for Modern Minimalistic events, or even an interactive garden arrangement for Enchanted Garden themes.",
                },
                {
                    "time": "2:30 - 3:30",
                    "activity": "Networking & Socializing",
                    "description": "Allow ample time for guests to mingle, enjoy the meal and explore interactive activity stations or photo booths that complement the theme.",
                },
                {
                    "time": "3:30 - 4:00",
                    "activity": "Closing Activity & Thank You",
                    "description": "Wrap up with a fun and memorable finale, such as a raffle draw, a group photo session in the themed photo booth, or a final performance (e.g., a live band or DJ set).",
                },
            ],
            "notes": "Maintain flexibility in timing; adjust durations based on guest engagement and the flow of the event. Consider having optional breakout sessions or quieter lounge areas for guests who prefer to relax.",
        },
    }
]

events = [
    {
        "event_title": "Mystery Book Club: And Then There Were None",
        "event_description": "Join us for a thrilling discussion of Agatha Christie's masterpiece 'And Then There Were None'. We'll explore the intricate plot twists and Christie's genius in crafting the perfect murder mystery.",
        "event_type": "book club",
        "event_is_public": True,
        "location": {
            "venue_name": "Riverside Community Library",
            "address": "123 Main Street, Seattle, WA 98101",
            "coordinates": {"lat": 47.6062, "lng": -122.3321},
            "indoor": True,
        },
        "event_status": "published",
        "event_date": "2025-02-15",
        "event_start": "14:00",
        "event_end": "16:00",
        "budget": 150,
        "guest_count": 15,
    },
    {
        "event_title": "Sarah's Baby Shower - Ocean Theme",
        "event_description": "Celebrate the upcoming arrival of baby Emma with an ocean-themed baby shower. Games, gifts, and seafood appetizers await!",
        "event_type": "baby shower",
        "event_is_public": False,
        "location": {
            "venue_name": "The Morrison Residence",
            "address": "456 Oak Avenue, Portland, OR 97204",
            "coordinates": {"lat": 45.5152, "lng": -122.6784},
            "indoor": True,
        },
        "event_status": "published",
        "event_date": "2025-03-08",
        "event_start": "11:00",
        "event_end": "14:30",
        "budget": 800,
        "guest_count": 25,
    },
    {
        "event_title": "Spring Gardening Workshop",
        "event_description": "Learn the basics of spring planting, soil preparation, and organic gardening techniques. Perfect for beginners and experienced gardeners alike.",
        "event_type": "gardening club",
        "event_is_public": True,
        "location": {
            "venue_name": "Green Thumb Gardens",
            "address": "789 Garden Way, Austin, TX 78701",
            "coordinates": {"lat": 30.2672, "lng": -97.7431},
            "indoor": False,
        },
        "event_status": "published",
        "event_date": "2025-03-22",
        "event_start": "10:00",
        "event_end": "12:30",
        "budget": 300,
        "guest_count": 20,
    },
    {
        "event_title": "Emily's 30th Birthday Bash",
        "event_description": "Join us for a Great Gatsby themed birthday celebration! Dress in your best 1920s attire for an evening of jazz, cocktails, and dancing.",
        "event_type": "birthday",
        "event_is_public": False,
        "location": {
            "venue_name": "The Roosevelt Ballroom",
            "address": "321 Broadway, New York, NY 10007",
            "coordinates": {"lat": 40.7128, "lng": -74.0060},
            "indoor": True,
        },
        "event_status": "published",
        "event_date": "2025-04-12",
        "event_start": "19:00",
        "event_end": "22:00",
        "budget": 2500,
        "guest_count": 30,
    },
    {
        "event_title": "Wine & Paint Night",
        "event_description": "Unleash your creativity while sipping on fine wines. Professional artist guidance provided. All materials included.",
        "event_type": "social",
        "event_is_public": True,
        "location": {
            "venue_name": "Artisan Studio",
            "address": "654 Artist Lane, San Francisco, CA 94102",
            "coordinates": {"lat": 37.7749, "lng": -122.4194},
            "indoor": True,
        },
        "event_status": "published",
        "event_date": "2025-02-28",
        "event_start": "18:00",
        "event_end": "20:30",
        "budget": 600,
        "guest_count": 18,
    },
]


@anvil.server.callable
def get_event():
    return events[0]


@anvil.server.callable
def get_events():
    return events


@anvil.server.callable
def get_ai_response():
    return ai_response

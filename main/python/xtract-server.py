import requests
import spacy
from spacy.matcher import Matcher
import re
from dotenv import load_dotenv
# Load small English model
nlp = spacy.load("en_core_web_sm")
import os
# Define common units
UNITS = {
    "cup", "cups", "c",
    "tablespoon", "tablespoons", "tb", "tbs", "tbsp",
    "teaspoon", "teaspoons", "ts", "tsp", "tspn",
    "gallon", "gallons", "gal", "gals",
    "ml", "mls", "milliliter", "milliliters",
    "l", "liters", "litres",
    "oz", "ounce", "ounces",
    "lb", "lbs", "pound", "pounds",
    "gram", "grams", "g", "kg", "kgs",
    "each", "large", "medium", "small", "can", "cans", "stick", "sticks", "bag", "bags"
}
# Word-to-number mapping
WORD_NUMBERS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "half": 0.5,
    "quarter": 0.25,
    # Add more as needed
}

# Converts a fraction string to float
def parse_fraction(s):
    s = s.strip()
    try:
        if ' ' in s:
            whole, frac = s.split()
            num, denom = frac.split('/')
            return float(whole) + float(num) / float(denom)
        elif '/' in s:
            num, denom = s.split('/')
            return float(num) / float(denom)
        else:
            return float(s)
    except:
        return None

# Function to extract the core ingredient name from full text
# Function to extract the core ingredient name from full text
def extract_core_name(full_name):
    # Check if this is a serving suggestion line
    if re.match(r'(?i).*serving suggestions.*', full_name):
        # For serving suggestions, prioritize extracting "chocolate milk" instead of "manhattan"
        if "chocolate milk" in full_name.lower():
            return "chocolate milk"
        # Otherwise extract what comes after "serving suggestions:"
        match = re.search(r'(?i)serving suggestions\s*:\s*(.*?)(?:\s+\(|\s+or\s+|\s*$)', full_name)
        if match:
            return match.group(1).strip()

    # Remove preparation instructions and additional details
    patterns = [
        r'\s+cut\s+into.*$',
        r'\s+peeled.*$',
        r'\s+melted.*$',
        r'\s+broken.*$',
        r'\s+beaten.*$',
        r'\s+chopped.*$',
        r'\s+sliced.*$',
        r'\s+diced.*$',
        r'\s+minced.*$',
        r'\s+grated.*$',
        r'\s+shredded.*$',
        r'\s+such\s+as.*$',
        r'\s+optional.*$',
        r'\s+plus.*$',
        r'\s+for\s+.*$',
        r'\s+or\s+.*$',
        r'\(.*?\)',  # Remove text in parentheses
        r',.*$',  # Remove anything after a comma
    ]

    core_name = full_name
    for pattern in patterns:
        core_name = re.sub(pattern, '', core_name, flags=re.IGNORECASE)

    return core_name.strip()

def extract_ingredients(text):
    ingredients = []
    lines = [i.strip() for i in re.split(r',\s*(?![^()]*\))', text)]

    for line in lines:
        original_line = line  # Store the original text for display_text
        doc = nlp(line)
        quantity = ''
        unit = ''
        name = ''
        display_text = ''

        # Handle "Juice of 2 lemons (about 1/4 cup)"
        juice_match = re.match(r'(?i)^(Juice|Zest|Peel)\s+of\s+(.*)', line)
        if juice_match:
            name = juice_match.group(1).strip().lower()
            rest = juice_match.group(2)
            # extract quantity like "2 lemons"
            qty_match = re.match(r'(\d+[ \d/]*\s*(?:\w+)?)', rest)
            if qty_match:
                quantity = qty_match.group(1).strip()
            remaining = rest.replace(qty_match.group(0), "").strip("() ")

            display_text = original_line  # Keep the full original text
            ingredient_name = f"{quantity.split(' ')[1]} {name}"  # e.g., "lemon juice"
            core_name = extract_core_name(ingredient_name)

            ingredients.append({
                "name": core_name,
                "display_text": f'{quantity.split(" ")[0]} {display_text}',
                "quantity": f'{quantity.split(" ")[0]}',
            })
            continue

        range_match = re.match(r'^(\d+(?:\s+\d+/\d+)?|\d+/\d+)\s*(?:to|-)\s*(\d+(?:\s+\d+/\d+)?|\d+/\d+)\s+(\w+)', line)
        if range_match:
            first = parse_fraction(range_match.group(1))
            second = parse_fraction(range_match.group(2))
            if first is not None and second is not None:
                larger_val = max(first, second)
                unit_candidate = range_match.group(3)
                if unit_candidate in UNITS:
                    unit = unit_candidate
                    after = line[range_match.end():].strip()
                    quantity = f"{range_match.group(2)} {unit}"
                    unit = f'{unit}'
                    name = after
                    display_text = original_line
                    core_name = extract_core_name(name)

                    ingredients.append({
                        "name": core_name,
                        "display_text": f"{quantity} {unit} {display_text}",
                        "quantity": quantity,
                        'unit': unit
                    })
                    continue
                else:
                    print(f"Skipping range line due to unit error: '{line}'")
            else:
                print(f"Skipping range line due to parse error: '{line}'")
                continue
        else:
            # Find the quantity (e.g., "1", "1/2", "1 1/2", "Six")
            quantity_match = re.match(r'^(\d+\s\d+/\d+|\d+/\d+|\d+|\w+)', line)
            if quantity_match:
                quantity_str = quantity_match.group(1).lower()
                # Convert word numbers to digits
                if quantity_str in WORD_NUMBERS:
                    quantity = WORD_NUMBERS[quantity_str]
                else:
                    quantity = quantity_str
                tokens = doc[len(quantity_str.split()):]
            else:
                tokens = doc

            tokens = [t.text for t in tokens]

            # Find the unit if it follows the quantity
            if tokens and tokens[0].lower() in UNITS:
                unit = tokens[0]
                tokens = tokens[1:]

            # The rest is the ingredient name
            name = ' '.join(tokens).strip()
            display_text = name  # This will be the full description with prep instructions

            # For the simplified name, remove preparation instructions
            core_name = extract_core_name(name)

            if core_name:
                ingredient = {
                    "name": core_name.lower(),
                    "display_text": f"{display_text.lower()}".strip() ,
                    "quantity": f"{quantity}".strip()
                }
                if unit:
                    ingredient["unit"] = unit
                    ingredient['display_text'] = unit +" "+ ingredient['display_text']
                ingredient['display_text'] = ingredient['quantity'] + " "+ ingredient['display_text']
                ingredients.append(ingredient)

    return ingredients

if __name__ == "__main__":
    load_dotenv()

    text = """
    2 cups all-purpose flour, 1/2 teaspoon salt, 6 ounces cold unsalted butter cut into cubes plus butter for the pie tin, 1/4 to 1/3 cup ice cold water, 1 stick (8 tablespoons) unsalted butter, 12 large apples such as Granny Smith peeled cored and sliced into eighths (about 14 cups), Juice of 2 lemons (about 1/4 cup), 1/4 cup loosely packed dark brown sugar, 1/4 cup loosely packed light brown sugar, 1/4 cup Southern Comfort, 1 tablespoon ground cinnamon, 1 large egg beaten with 2 tablespoons water, Nonstick canola oil spray, 1 pound marshmallow creme, 4 tablespoons unsalted butter melted and cooled, 1/2 cup powdered sugar, 1/3 cup miniature chocolate-covered candies such as M and M's plus more for garnish, 2 tablespoons bourbon, 1 teaspoon vermouth, 1 teaspoon grenadine, 24 whole graham crackers each broken carefully in half, 80 stackable marshmallows (2 bags), Six 4-ounce bars high-quality semisweet chocolate chopped, Optional serving suggestions: Manhattan's (for the adults) or chocolate milk (for the kids)
    """

    parsed = extract_ingredients(text)

    for item in parsed:
        print(item)

    # Build payload for POST request
    payload = {
        "title": "1 Smore for the Road and Kiddie Smores",
        "image_url": "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2013/5/10/0/ZB0403H_kiddie-smores-recipe_s4x3.jpg.rend.hgtvcom.1280.720.suffix/1371616409601.jpeg",
        "expires_in": 1,
        "instructions": [
            "1 : Coat a large microwave-safe bowl with nonstick spray. Add the marshmallow creme and microwave until warmed through and slightly puffed, 30 to 45 seconds. Add the butter and powdered sugar and whip with a hand mixer until light and fluffy, 1 to 2 minutes. Transfer half of the mixture to another bowl coated with nonstick spray and fold in the candies. Set aside until ready to use.",
            "2 : Add the bourbon, vermouth and grenadine to the remaining marshmallow mixture and whip with a hand mixer until well combined. Set aside until ready to use.",
            '3 : To build the "1 smore for the road": On a cooling rack over a half baking sheet, lay down 32 of the graham cracker halves. Spread 1 1/2 teaspoons of the "Manhattan(" marshmallow creme on each graham cracker half. Place 4 stackable marshmallows on 16 of the graham cracker halves. Top with the remaining graham cracker halves.',
    '4 : To build the kiddie smores: On a cooling rack over a half baking sheet, lay down the remaining 16 graham cracker halves. Spread 1 tablespoon of ")kiddie" marshmallow creme on each graham cracker half. Place 2 stackable marshmallows on 8 of the graham cracker halves. Top with the remaining graham cracker halves.',
            '5 : In a metal bowl set over a saucepan with about 1 inch of simmering water in it, melt the semisweet chocolate over medium-low heat until completely smooth, stirring constantly, 5 to 7 minutes. Once the chocolate is melted, turn the heat off below the pan. Pour 2 tablespoons of the melted chocolate on top of each smore, letting the chocolate drip down the sides. Once the smores are finished, let the chocolate harden at room temperature for an hour (or if you are in a hurry, then let set up in the refrigerator for 15 minutes). ',
            '6 : Serve with a side of Manhattans for the adults and some chocolate milk for the kids. '
    ],
        "line_items": parsed
    }
    api_key = os.getenv("API_KEY")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://connect.dev.instacart.tools/idp/v1/products/products_link",
        headers=headers,
        json=payload
    )

    print("POST response:", response.status_code)
    print(response.json())
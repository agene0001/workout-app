import requests
import spacy
from spacy.matcher import Matcher
import re
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
# Load environment variables
load_dotenv()

# Initialize Flask app

recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')
# Load small English model
nlp = spacy.load("en_core_web_sm")

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
QUANTIY_ERRORS = ['ice']
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
        r'\s+thinly\s+sliced.*$',
        r'\s+finely\s+minced.*$',
        r'\s+roughly\s+chopped.*$',
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
        dash_pattern = re.match(r'^(\d+(?:\s+\d+/\d+)?|\d+/\d+)\s*-\s*(\w+)\s+(.*)', line)
        if dash_pattern:
            quantity = dash_pattern.group(1).strip()
            unit = dash_pattern.group(2).strip()
            name = dash_pattern.group(3).strip()
            display_text = original_line
            core_name = extract_core_name(name)

            ingredients.append({
                "name": core_name.lower(),
                "display_text": display_text.lower(),
                "quantity": quantity,
                "unit": unit
            })
            continue
        # Special handling for optional serving suggestions
        if re.match(r'(?i)optional\s+serving\s+suggestions.*', line):
            display_text = original_line.lower()
            # Specifically extract chocolate milk for name
            name = "chocolate milk"
            ingredients.append({
                "name": name.lower(),
                "display_text": display_text,
                "quantity": "optional"
            })
            continue

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
                elif quantity_str in QUANTIY_ERRORS:
                    quantity = ""
                    name = quantity_str+" "
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
            name += ' '.join(tokens).strip()
            display_text = name  # This will be the full description with prep instructions

            # For the simplified name, remove preparation instructions
            core_name = extract_core_name(name)
            if core_name:
                ingredient = {
                    "name": core_name.lower(),
                    "display_text": f"{display_text.lower()}".strip(),
                    "quantity": f"{quantity}".strip()
                }
                if unit:
                    ingredient["unit"] = unit
                    ingredient['display_text'] = unit + " " + ingredient['display_text']
                ingredient['display_text'] = ingredient['quantity'] + " " + ingredient['display_text']
                ingredients.append(ingredient)

    return ingredients

def process_recipe(ingredients_text, instructions, title, image_url=""):
    """Process recipe ingredients and instructions and send to Instacart API"""

    # Extract ingredients
    parsed_ingredients = extract_ingredients(ingredients_text)

    # Build payload for POST request
    payload = {
        "title": title,
        "image_url": image_url,
        "expires_in": 1,
        "instructions": instructions,
        "line_items": parsed_ingredients
    }
    print(payload)
    # Get API key from environment
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
    try:
        data = response.json()
    except ValueError:
        print("Response was not valid JSON.")
        data = None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
        data = None
    except requests.exceptions.Timeout:
        print("The request timed out.")
        data = None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        data = None

    return {
        "status_code": response.status_code,
        "response": data,
        "processed_ingredients": parsed_ingredients
    }
app = Flask(__name__)

# API routes
@recipe_bp.route('/process-recipe', methods=['POST'])
def process_recipe_api():
    """API endpoint to process recipe ingredients and instructions"""
    try:
        data = request.json

        # Check for required fields
        if 'title' not in data:
            return jsonify({"error": "Missing name field"}), 400
        if 'ingredients' not in data:
            return jsonify({"error": "Missing ingredients field"}), 400
        if 'instructions' not in data:
            return jsonify({"error": "Missing instructions field"}), 400

        # Extract optional fields
        title = data.get('title', 'Recipe')
        image_url = data.get('image_url', '')

        # Process ingredients and instructions
        result = process_recipe(
            data['ingredients'],
            data['instructions'],
            title,
            image_url
        )

        return jsonify(result),200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
app.register_blueprint(recipe_bp)
CORS(app)  # This allows all domains, you can restrict it if needed

# Simple health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    host=  os.getenv("NODE_ENV","dev")
    if host== "production":
        # debug off so wont see explanatory information in dockercompose or kubernetes
        app.run(debug=True, host='0.0.0.0', port=8082)
    elif host == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5000)

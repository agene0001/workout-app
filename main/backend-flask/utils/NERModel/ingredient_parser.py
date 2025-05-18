# ingredient_parser.py
import re

import spacy
from pathlib import Path

# --- Re-use helper functions from your old parser ---
# You'll need WORD_NUMBERS and parse_fraction here.
# You can either copy them directly or import them if they are in a utils file.

WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "half": 0.5, "quarter": 0.25,
    "a": 1, "an": 1,
}

def parse_fraction(s):
    s = s.strip()
    try:
        if ' ' in s:
            parts = s.split()
            if len(parts) == 2 and '/' in parts[1]:
                whole, frac = parts
                num, denom = frac.split('/')
                return float(whole) + float(num) / float(denom)
            else:
                return float(parts[0])
        elif '/' in s:
            num, denom = s.split('/')
            return float(num) / float(denom)
        else:
            return float(s)
    except (ValueError, ZeroDivisionError):
        # Check if it's a word number before returning None
        val = WORD_NUMBERS.get(s.lower())
        if val is not None:
            return float(val)
        return None

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "ingredient_ner_model"
NLP_CUSTOM = None # Global variable to hold the loaded model

def load_model(model_path=MODEL_PATH):
    """Loads the custom spaCy NER model."""
    global NLP_CUSTOM
    if NLP_CUSTOM is None: # Load only once
        if model_path.exists():
            NLP_CUSTOM = spacy.load(model_path)
            print(f"Loaded custom NER model from {model_path}")
        else:
            print(f"ERROR: Model not found at {model_path}. Please train the model first.")
            # Fallback or raise error
            # For now, let's try loading a base spaCy model as a dummy
            # In a real app, you'd handle this more gracefully or ensure the model exists.
            print("Warning: Custom model not found. Falling back to en_core_web_sm (will not perform custom NER).")
            try:
                NLP_CUSTOM = spacy.load("en_core_web_sm")
            except OSError:
                print("Downloading en_core_web_sm as fallback...")
                spacy.cli.download("en_core_web_sm")
                NLP_CUSTOM = spacy.load("en_core_web_sm")
    return NLP_CUSTOM


# ingredient_parser.py
import re
import spacy # Assuming spacy and re are needed by other parts of your file
# ... (other necessary imports like Path, and your helper functions like parse_fraction)

# Make sure parse_fraction is defined if it's not already
# For example:
# def parse_fraction(s):
#     # ... your implementation ...
#     return float_value_or_None

def format_extracted_entities(doc, original_text):
    parsed_item = {}

    temp_name_parts = []
    temp_quantity_text = None
    temp_unit_text = None

    last_core_entity_end_char = 0 # This variable determines the end of the display_text

    parenthetical_qty = None
    parenthetical_unit = None
    is_juice_pattern = False
    juice_subject_parts = [] # To store "lemons" if "Juice" is first
    # core_entity_texts_in_order is not used in your original function for display_text construction
    # so we can ignore it for this minimal change.

    for ent in doc.ents:
        paren_phrases_spans = [(m.start(), m.end()) for m in re.finditer(r'\([^)]*\)', original_text)]
        is_part_of_paren_phrase = any(p_start <= ent.start_char and ent.end_char <= p_end for p_start, p_end in paren_phrases_spans)

        if ent.label_ == "QTY":
            if not is_part_of_paren_phrase and temp_quantity_text is None:
                temp_quantity_text = ent.text
            elif is_part_of_paren_phrase and parenthetical_qty is None:
                parenthetical_qty = ent.text
            # elif temp_quantity_text is None and parenthetical_qty is not None: # This line was redundant with the next one
            #     temp_quantity_text = parenthetical_qty

            # CRITICAL: QTY entities should always extend the last_core_entity_end_char
            # Your original code only did this for non-parenthetical.
            # Let's assume all QTY, UNIT, NAME, ALT_NAME can potentially extend it.
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)


        elif ent.label_ == "UNIT":
            if not is_part_of_paren_phrase and temp_unit_text is None:
                temp_unit_text = ent.text
            elif is_part_of_paren_phrase and parenthetical_unit is None:
                parenthetical_unit = ent.text
            # elif temp_unit_text is None and parenthetical_unit is not None: # Redundant
            #     temp_unit_text = parenthetical_unit

            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        elif ent.label_ == "NAME":
            temp_name_parts.append(ent.text)
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        # ------------------------------------------------------------------ #
        # MINIMAL CHANGE: Add ALT_NAME handling HERE                       #
        # ------------------------------------------------------------------ #
        elif ent.label_ == "ALT_NAME":
            # The text of ALT_NAME is not directly stored in a temp variable here
            # because it's only used to extend the display_text via its end character.
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)
        # ------------------------------------------------------------------ #

        # Your original code did not have explicit handling for COMMENT or PREP
        # in terms of updating last_core_entity_end_char.
        # So, we'll keep it that way for a minimal change. The display_text
        # will be defined by the last QTY, UNIT, NAME, or ALT_NAME.

    # ---- Logic to decide which QTY/UNIT to use (remains the same) ----
    if temp_quantity_text is None and parenthetical_qty is not None:
        temp_quantity_text = parenthetical_qty
    if temp_unit_text is None and parenthetical_unit is not None:
        temp_unit_text = parenthetical_unit

    # Reconstruct display_text (logic remains mostly the same, relies on last_core_entity_end_char)
    # The loop `for ent in doc.ents: if ent.label_ in ["QTY", "UNIT", "NAME"]:`
    # that you had later for `has_core_entities` was a bit redundant if the first loop
    # already sets `last_core_entity_end_char` based on these (and now ALT_NAME).

    if last_core_entity_end_char > 0: # If any QTY, UNIT, NAME, or ALT_NAME was found
        display_text_candidate = original_text[:last_core_entity_end_char].strip()
        parsed_item["display_text"] = display_text_candidate.rstrip(',').strip()
    else:
        # No QTY, UNIT, NAME, or ALT_NAME entities found that set last_core_entity_end_char.
        # This would happen for "salt" or if NER fails.
        parsed_item["display_text"] = original_text.strip()


    # Process quantity (using temp_quantity_text which should be the prioritized one)
    if temp_quantity_text:
        # Ensure parse_fraction is defined
        parsed_q = parse_fraction(temp_quantity_text)
        if parsed_q is not None:
            if parsed_q == int(parsed_q):
                parsed_item["quantity"] = str(int(parsed_q))
            else:
                parsed_item["quantity"] = f"{parsed_q:.3f}".rstrip('0').rstrip('.')
        else:
            parsed_item["quantity"] = temp_quantity_text
    else:
        parsed_item["quantity"] = ""

    if temp_unit_text:
        parsed_item["unit"] = temp_unit_text.lower()

    name_str = " ".join(temp_name_parts).strip()
    if name_str:
        parsed_item["name"] = name_str
    else:
        if not doc.ents and len(original_text.split()) <= 3 :
            parsed_item["name"] = original_text.strip()
            # If display_text wasn't set by last_core_entity_end_char, ensure it's set
            if not parsed_item.get("display_text") or last_core_entity_end_char == 0:
                parsed_item["display_text"] = original_text.strip()
        else:
            parsed_item["name"] = ""

    # Fallback for display_text if still not set (should be rare now)
    if not parsed_item.get("display_text"):
        parsed_item["display_text"] = original_text.strip()


    # Ensure 'quantity' and 'name' keys exist
    if "quantity" not in parsed_item: parsed_item["quantity"] = ""
    if "name" not in parsed_item: parsed_item["name"] = ""


    # Final check for validity (remains the same)
    is_valid_ingredient = False
    if parsed_item.get("name"):
        is_valid_ingredient = True
    elif parsed_item.get("quantity") and parsed_item.get("unit"):
        is_valid_ingredient = True

    if not is_valid_ingredient:
        if not doc.ents and len(parsed_item.get("display_text","").split()) <=2:
            parsed_item["name"] = parsed_item.get("display_text","")
            is_valid_ingredient = True

    if not is_valid_ingredient:
        return None

    return parsed_item
def parse_single_ingredient_line(ingredient_line):
    """
    Parses a single ingredient line using the custom NER model.
    """
    nlp_model = load_model() # Ensures model is loaded
    if nlp_model is None: # Should ideally not happen if load_model handles fallback
        print("Error: NLP model could not be loaded.")
        return {"display_text": ingredient_line, "name": ingredient_line, "quantity": "", "unit": ""}

    doc = nlp_model(ingredient_line.strip())
    # print(f"DEBUG: For line '{ingredient_line}', NER entities:")
    # for ent in doc.ents:
    #     print(f"  Text: '{ent.text}', Label: '{ent.label_}'")

    return format_extracted_entities(doc, ingredient_line)


# --- This is the main function your Flask app will call ---
def extract_ingredients_ner(ingredients_list_raw):
    """
    Processes a list of raw ingredient strings and parses them.
    This replaces your old `extract_ingredients` function.
    """
    if not isinstance(ingredients_list_raw, list):
        # Handle cases where a single string might be passed
        if isinstance(ingredients_list_raw, str):
            ingredients_list_raw = [ingredients_list_raw]
        else:
            print("Input must be a list of strings.")
            return []

    parsed_ingredients = []

    # Pre-processing steps from your old parser (like 'and' splitting) can go here if desired.
    # For simplicity, we'll parse each line as is first.
    # You might want to re-integrate your 'and' splitting logic:
    processed_lines = []
    for line_input in ingredients_list_raw:
        # --- Your "and" splitting logic from OLD_INGREDIENTS_PARSER ---
        # (Slightly simplified for brevity here, copy your full logic)
        if "salt and pepper" in line_input.lower(): # Example, make more robust
            processed_lines.append(line_input) # Treat as one
        elif " and " in line_input and not re.search(r'\([^)]*and[^)]*\)', line_input): # From your old code
            parts = line_input.split(" and ")
            for part in parts:
                if part.strip():
                    processed_lines.append(part.strip())
        else:
            processed_lines.append(line_input.strip())

    for line in processed_lines:
        if not line.strip():
            continue

        line_lower = line.lower() # Work with a lowercased version for startswith checks

        # Handle "for the garnish:" specifically
        if line_lower.startswith("for the garnish:"):
            garnish_item_text = line.split(":", 1)[1].strip()
            if garnish_item_text: # Ensure there's something after the colon
                parsed_item = parse_single_ingredient_line(garnish_item_text)
                if parsed_item:
                    # The expected display_text is the full original line
                    parsed_item["display_text"] = line.strip()
                    # The name should be from the parsed garnish_item_text
                    # quantity and unit might also come from parsing garnish_item_text
                    parsed_ingredients.append(parsed_item)
            continue # Move to the next line after handling "for the garnish:"

        # Handle other headers/instructions that should be skipped
        elif line_lower.startswith(("instructions:", "notes:")): # "for the" (generic) removed
            continue

        # Handle lines that *only* start with "garnish:" (not "for the garnish:")
        elif line_lower.startswith("garnish:"):
            garnish_item_text = line.split(":", 1)[1].strip()
            if garnish_item_text:
                parsed_item = parse_single_ingredient_line(garnish_item_text)
                if parsed_item:
                    parsed_item["display_text"] = line.strip()
                    parsed_ingredients.append(parsed_item)
            continue

        # If it's not a special header, parse as a regular ingredient
        parsed_item = parse_single_ingredient_line(line)
        if parsed_item:
            parsed_ingredients.append(parsed_item)
        else:
            print(f"Warning: Could not parse line into structured format: '{line}'")


    return parsed_ingredients

if __name__ == '__main__':
    # Example usage:
    print("--- Testing ingredient_parser.py ---")
    load_model() # Load the model

    test_ingredients1 = ["1/2 cup finely chopped pecans, for garnish", "2 large eggs", "salt"]
    parsed1 = extract_ingredients_ner(test_ingredients1)
    print("\nParsed Set 1:")
    for item in parsed1:
        print(item)

    test_ingredients2 = ["1 (15-ounce) can black beans, rinsed and drained"]
    parsed2 = extract_ingredients_ner(test_ingredients2)
    print("\nParsed Set 2:")
    for item in parsed2:
        print(item)

    test_ingredients3 = ["Juice of 2 lemons (about 1/4 cup)"] # This will be challenging without specific 'juice of' logic
    parsed3 = extract_ingredients_ner(test_ingredients3)
    print("\nParsed Set 3 (Challenging Case):")
    for item in parsed3:
        print(item)
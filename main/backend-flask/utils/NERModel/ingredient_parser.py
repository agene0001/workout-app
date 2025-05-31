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
MODEL_PATH = PROJECT_ROOT / "models" / "ingredient_ner_model_patience_stop" / "model_final"
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
#  UNIT CAN HAVE mediumtolarge,medium-sized, ounces/4, cups/500, fluid ounces/,-ounce. MUST PARSE
def format_extracted_entities(doc, original_text):
    # Initialize parsed_item with new fields for alternative quantity and unit
    parsed_item = {
        "quantity": "",
        "alternative_quantity": "", # NEW FIELD
        "unit": "",
        "alternative_unit": "",   # NEW FIELD
        "name": "",
        "alternative_name": "",   # Existing, for alternative names
        "preparation": [],        # Keeping as list for now
        "comment": [],            # Keeping as list for now
        "display_text": original_text.strip()
    }

    temp_name_parts = []
    temp_quantity_text = None
    temp_unit_text = None
    primary_unit_candidate = None
    last_core_entity_end_char = 0

    parenthetical_qty = None
    parenthetical_unit = None
    # is_juice_pattern = False # Not used in provided function
    # juice_subject_parts = [] # Not used in provided function

    # Ensure entities are sorted by start character to process them in order
    # This helps with logic that might depend on the order of appearance.
    sorted_ents = sorted(doc.ents, key=lambda ent: ent.start_char)

    for ent in sorted_ents: # Iterate through sorted entities
        paren_phrases_spans = [(m.start(), m.end()) for m in re.finditer(r'\([^)]*\)', original_text)]
        is_part_of_paren_phrase = any(p_start <= ent.start_char and ent.end_char <= p_end for p_start, p_end in paren_phrases_spans)

        if ent.label_ == "QTY":
            if not is_part_of_paren_phrase and temp_quantity_text is None:
                temp_quantity_text = ent.text
            elif is_part_of_paren_phrase and parenthetical_qty is None:
                parenthetical_qty = ent.text
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        elif ent.label_ == "UNIT":
            raw_unit_text = ent.text.lower().strip().rstrip('.') # Normalize: lowercase, strip, remove trailing dot
            parsed_unit_candidate = raw_unit_text # What we'll try to match against allowed units

            # 1. Handle compound units with slashes or specific patterns first
            if "/" in raw_unit_text:
                # e.g., "ounces/4", "cups/500", "fluid ounces/..."
                # The part before the slash is usually the primary unit
                parsed_unit_candidate = raw_unit_text.split('/', 1)[0].strip()
                # You might want to store the part after "/" if it's meaningful, e.g., in an alt_qty or comment
                # print(f"DEBUG: Split unit '{raw_unit_text}' into primary '{parsed_unit_candidate}'")
            elif raw_unit_text == "-ounce": # Handle "-ounce" specifically, often part of e.g., "16-ounce can"
                parsed_unit_candidate = "ounce" # Normalize to "ounce"
            elif raw_unit_text.endswith("-sized"): # e.g., "medium-sized"
                parsed_unit_candidate = raw_unit_text # Keep as "medium-sized" if that's an allowed unit
            elif raw_unit_text == "mediumtolarge": # Handle specific combined terms
                parsed_unit_candidate = "medium-large" # Normalize to a more standard form or keep as is if allowed

            # 2. Assign to primary_unit_candidate or parenthetical_unit_candidate
            if not is_part_of_paren_phrase:
                if primary_unit_candidate is None:
                    primary_unit_candidate = parsed_unit_candidate
            elif is_part_of_paren_phrase:
                if parenthetical_unit_candidate is None:
                    parenthetical_unit_candidate = parsed_unit_candidate

            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        elif ent.label_ == "NAME":
            temp_name_parts.append(ent.text)
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        elif ent.label_ == "ALT_NAME": # This is for alternative *ingredient names*
            # Store the first encountered ALT_NAME directly
            if not parsed_item["alternative_name"]:
                parsed_item["alternative_name"] = ent.text
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        # --- ADDED/MODIFIED SECTION for ALT_QTY and ALT_UNIT ---
        elif ent.label_ == "ALT_QTY":
            if not parsed_item["alternative_quantity"]: # Take the first one found
                parsed_item["alternative_quantity"] = ent.text
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char) # Ensure it contributes to display_text

        elif ent.label_ == "ALT_UNIT":
            if not parsed_item["alternative_unit"]: # Take the first one found
                parsed_item["alternative_unit"] = ent.text
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char) # Ensure it contributes to display_text
        # --- END OF ADDED/MODIFIED SECTION ---

        elif ent.label_ == "PREP": # Added for completeness if you intend to use it
            parsed_item["preparation"].append(ent.text)
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char) # PREP can be part of display text

        elif ent.label_ == "COMMENT": # Added for completeness
            parsed_item["comment"].append(ent.text)
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char) # COMMENT can be part of display text


    # Prioritize non-parenthetical QTY/UNIT, then parenthetical if primary is missing
    if temp_quantity_text is None and parenthetical_qty is not None:
        temp_quantity_text = parenthetical_qty
    if temp_unit_text is None and parenthetical_unit is not None: # temp_unit_text would have been lowercased already if set
        temp_unit_text = parenthetical_unit # parenthetical_unit was also lowercased if set

    # Construct display_text
    # last_core_entity_end_char is now updated by QTY, UNIT, NAME, ALT_NAME, ALT_QTY, ALT_UNIT, PREP, COMMENT
    if last_core_entity_end_char > 0:
        display_text_candidate = original_text[:last_core_entity_end_char].strip()
        parsed_item["display_text"] = display_text_candidate.rstrip(',').strip()
    else:
        parsed_item["display_text"] = original_text.strip()


    if temp_quantity_text:
        parsed_q = parse_fraction(temp_quantity_text)
        if parsed_q is not None:
            parsed_item["quantity"] = str(int(parsed_q)) if parsed_q == int(parsed_q) else f"{parsed_q:.3f}".rstrip('0').rstrip('.')
        else:
            parsed_item["quantity"] = temp_quantity_text
    # else: parsed_item["quantity"] = "" # Already initialized

    if temp_unit_text: # Already lowercased during assignment
        parsed_item["unit"] = temp_unit_text.strip().rstrip('.') # Ensure stripped and no trailing dot
    # else: parsed_item["unit"] = "" # Already initialized


    name_str = " ".join(temp_name_parts).strip() # This only contains text from NAME entities
    if name_str:
        parsed_item["name"] = name_str
    elif not doc.ents and len(original_text.split()) <= 3 :
        parsed_item["name"] = original_text.strip()
        if not parsed_item.get("display_text") or last_core_entity_end_char == 0:
            parsed_item["display_text"] = original_text.strip()
    # else: parsed_item["name"] = "" # Already initialized

    # Fallback for display_text if it somehow got emptied or was never set properly
    if not parsed_item.get("display_text"):
        parsed_item["display_text"] = original_text.strip()

    # Join preparation and comment lists
    parsed_item["preparation"] = ", ".join(p for p in parsed_item["preparation"] if p)
    parsed_item["comment"] = ". ".join(c for c in parsed_item["comment"] if c)


    # Final check for validity
    is_valid_ingredient = False
    if parsed_item.get("name"):
        is_valid_ingredient = True
    elif parsed_item.get("quantity") and parsed_item.get("unit"): # Unit must be populated
        is_valid_ingredient = True

    if not is_valid_ingredient:
        if not doc.ents and len(parsed_item.get("display_text","").split()) <=2:
            if not parsed_item["name"]: # Check again
                parsed_item["name"] = parsed_item.get("display_text","")
            is_valid_ingredient = True # if it's a short unparsed string, treat it as a valid name

    return parsed_item if is_valid_ingredient else None

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
        # elif " and " in line_input and not re.search(r'\([^)]*and[^)]*\)', line_input): # From your old code
        #     parts = line_input.split(" and ")
        #     for part in parts:
        #         if part.strip():
        #             processed_lines.append(part.strip())
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
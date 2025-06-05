# ingredient_parser.py
import re
import spacy
from pathlib import Path
import time # For benchmarking

# --- Re-use helper functions from your old parser ---
WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 12,
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
        val = WORD_NUMBERS.get(s.lower())
        if val is not None:
            return float(val)
        return None

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "ingredient_ner_model_patience_stop" / "model_final"

NLP_CUSTOM = None # Global variable to hold the loaded model

def load_model(model_path=MODEL_PATH):
    """Loads the custom spaCy NER model only once."""
    global NLP_CUSTOM
    if NLP_CUSTOM is None: # Load only once
        if model_path.exists():
            try:
                # Crucial for speed: Disable pipeline components not needed for your NER task.
                # If your custom model only performs NER, you don't need tagger, parser, etc.
                # Adjust this list based on what components your custom model actually contains and needs.
                # Common components to disable if only NER is needed:
                # "tagger", "parser", "attribute_ruler", "lemmatizer", "textcat"
                # If your custom model was specifically trained ONLY for NER, it might not even have these.
                # In that case, spacy.load() might still be faster if you specify them here.
                components_to_disable = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "textcat", "senter"]
                NLP_CUSTOM = spacy.load(model_path, disable=components_to_disable)
                print(f"Loaded custom NER model from {model_path} with disabled components: {', '.join(components_to_disable)}")
            except ValueError as e:
                # This can happen if the model doesn't have some of the components you tried to disable.
                # In that case, load the model without explicit disabling.
                print(f"Warning: Could not disable all specified components for model at {model_path} ({e}). Attempting to load without explicit disabling.")
                NLP_CUSTOM = spacy.load(model_path)
                print(f"Loaded custom NER model from {model_path} (without explicit component disabling).")
            except Exception as e:
                print(f"ERROR: Failed to load custom model from {model_path}: {e}")
                print("Falling back to en_core_web_sm (will not perform custom NER).")
                try_load_fallback_model()
        else:
            print(f"ERROR: Custom model not found at {model_path}.")
            print("Falling back to en_core_web_sm (will not perform custom NER).")
            try_load_fallback_model()
    return NLP_CUSTOM

def try_load_fallback_model():
    """Helper to load or download fallback spaCy model."""
    global NLP_CUSTOM
    try:
        # Fallback model, generally slower for just NER as it's a full pipeline
        NLP_CUSTOM = spacy.load("en_core_web_sm")
        print("Loaded fallback model: en_core_web_sm.")
    except OSError:
        print("Downloading en_core_web_sm as fallback...")
        try:
            spacy.cli.download("en_core_web_sm")
            NLP_CUSTOM = spacy.load("en_core_web_sm")
            print("Successfully downloaded and loaded fallback model: en_core_web_sm.")
        except Exception as e:
            print(f"CRITICAL ERROR: Could not download or load en_core_web_sm: {e}")
            NLP_CUSTOM = None # Ensure it's None if even fallback fails


# Pre-compile regex patterns for performance
PARENTHETICAL_REGEX = re.compile(r'\([^)]*\)')
UNIT_DASH_NUMBER_REGEX = re.compile(r'-\d+$')
def format_extracted_entities(doc, original_text):
    """
    Extracts entities from a spaCy Doc object and formats them into the desired dictionary structure.
    All recognized entities contribute to the 'display_text'.
    """
    parsed_item = {
        "quantity": "",
        "unit": "",
        "name": "",
        "display_text": original_text.strip() # Initialize with full text as fallback
    }

    temp_name_parts = []
    temp_quantity_text = None
    primary_unit_candidate = None
    parenthetical_qty = None
    parenthetical_unit = None
    last_core_entity_end_char = 0 # Tracks the furthest character position of any recognized entity

    sorted_ents = sorted(doc.ents, key=lambda ent: ent.start_char)
    paren_phrases_spans = [(m.start(), m.end()) for m in PARENTHETICAL_REGEX.finditer(original_text)]

    for ent in sorted_ents:
        is_part_of_paren_phrase = any(p_start <= ent.start_char and ent.end_char <= p_end for p_start, p_end in paren_phrases_spans)

        if ent.label_ == "QTY":
            if not is_part_of_paren_phrase and temp_quantity_text is None:
                temp_quantity_text = ent.text
            elif is_part_of_paren_phrase and parenthetical_qty is None:
                parenthetical_qty = ent.text
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        elif ent.label_ == "UNIT":
            raw_unit_text = ent.text.lower().strip().rstrip('.')
            parsed_unit_candidate = raw_unit_text

            if "/" in raw_unit_text:
                parsed_unit_candidate = raw_unit_text.split('/', 1)[0].strip()
            elif raw_unit_text == "-ounce" or raw_unit_text == "-ounces":
                parsed_unit_candidate = "ounce"
            elif raw_unit_text == "largest-available":
                parsed_unit_candidate = "large"
            elif raw_unit_text == "-cup" or raw_unit_text == "-cups":
                parsed_unit_candidate = "cup"
            elif raw_unit_text.endswith("-sized"):
                parsed_unit_candidate = raw_unit_text
            elif raw_unit_text == "mediumtolarge":
                parsed_unit_candidate = "medium-large"
            elif UNIT_DASH_NUMBER_REGEX.search(raw_unit_text):
                parsed_unit_candidate = UNIT_DASH_NUMBER_REGEX.sub('', raw_unit_text).strip()

            if not is_part_of_paren_phrase:
                if primary_unit_candidate is None:
                    primary_unit_candidate = parsed_unit_candidate
            elif is_part_of_paren_phrase:
                if parenthetical_unit is None:
                    parenthetical_unit = parsed_unit_candidate

            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        elif ent.label_ == "NAME":
            temp_name_parts.append(ent.text)
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

        # All other entities contribute to display_text length but not specific fields
        elif ent.label_ in ["ALT_NAME", "ALT_QTY", "ALT_UNIT"]:
            last_core_entity_end_char = max(last_core_entity_end_char, ent.end_char)

    # Determine final primary quantity and unit
    if temp_quantity_text is None and parenthetical_qty is not None:
        temp_quantity_text = parenthetical_qty

    temp_unit_text = None
    if primary_unit_candidate:
        temp_unit_text = primary_unit_candidate
    elif parenthetical_unit:
        temp_unit_text = parenthetical_unit

    # Construct display_text
    if last_core_entity_end_char > 0:
        display_text_candidate = original_text[:last_core_entity_end_char].strip()
        parsed_item["display_text"] = display_text_candidate.rstrip(',').strip()
    else:
        parsed_item["display_text"] = original_text.strip()

    # Parse and assign quantity
    if temp_quantity_text:
        parsed_q = parse_fraction(temp_quantity_text)
        if parsed_q is not None:
            parsed_item["quantity"] = str(int(parsed_q)) if parsed_q == int(parsed_q) else f"{parsed_q:.3f}".rstrip('0').rstrip('.')
        else:
            parsed_item["quantity"] = temp_quantity_text

    # Assign unit (already normalized)
    if temp_unit_text:
        parsed_item["unit"] = temp_unit_text.strip().rstrip('.')

    # Join name parts
    name_str = " ".join(temp_name_parts).strip()
    if name_str:
        parsed_item["name"] = name_str
    elif not doc.ents and len(original_text.split()) <= 3 :
        parsed_item["name"] = original_text.strip()
        if not parsed_item.get("display_text") or last_core_entity_end_char == 0:
            parsed_item["display_text"] = original_text.strip()

    is_valid_ingredient = False
    if parsed_item.get("name"):
        is_valid_ingredient = True
    elif parsed_item.get("quantity") and parsed_item.get("unit"):
        is_valid_ingredient = True

    if not is_valid_ingredient:
        if not doc.ents and len(parsed_item.get("display_text","").split()) <= 2:
            if not parsed_item["name"]:
                parsed_item["name"] = parsed_item.get("display_text","")
            is_valid_ingredient = True

    return parsed_item if is_valid_ingredient else None


def extract_ingredients_ner(ingredients_list_raw):
    """
    Processes a list of raw ingredient strings and parses them using spaCy's nlp.pipe for speed.
    """
    # Load the model ONCE at the beginning of the main function
    nlp_model = load_model()
    if nlp_model is None:
        print("Critical Error: NLP model could not be loaded. Aborting parsing.")
        return []

    if not isinstance(ingredients_list_raw, list):
        if isinstance(ingredients_list_raw, str):
            ingredients_list_raw = [ingredients_list_raw]
        else:
            print("Input must be a list of strings.")
            return []

    parsed_ingredients = []
    # Store tuples of (original_line_for_display, text_for_nlp_processing, is_garnish_header_flag, original_index)
    # original_index is added to maintain output order if needed, though zip keeps order too.
    texts_for_nlp_pipe_with_context = []
    nlp_input_texts = [] # This list will hold the actual strings passed to nlp.pipe

    for i, line_input in enumerate(ingredients_list_raw):
        line = line_input.strip()
        if not line:
            continue

        line_lower = line.lower()
        text_to_process = line # Default
        is_garnish_header_line = False
        skip_nlp_processing = False # Flag for lines not needing NLP

        if "salt and pepper" in line_lower:
            # Special case for "salt and pepper" - process as one
            pass # Keep text_to_process as full line
        # Add any other "and" splitting logic here if needed. For this example, keeping simple.
        # elif " and " in line and not re.search(r'\([^)]*and[^)]*\)', line):
        #     # This logic would require splitting and potentially adding multiple items for one original line
        #     # which complicates the 1:1 mapping for nlp.pipe results.
        #     # For this example, we'll avoid splitting for batching efficiency directly here.
        #     pass

        # Handle specific header/instruction lines that should be skipped or only partially processed
        if line_lower.startswith("for the garnish:"):
            text_to_process = line.split(":", 1)[1].strip()
            is_garnish_header_line = True
        elif line_lower.startswith(("instructions:", "notes:")):
            skip_nlp_processing = True # These lines are skipped entirely from NLP
        elif line_lower.startswith("garnish:"):
            text_to_process = line.split(":", 1)[1].strip()
            is_garnish_header_line = True

        if skip_nlp_processing:
            continue # Move to the next line

        # If text_to_process is empty after splitting (e.g., "garnish: "), or if it's just a header,
        # we might want to handle it as a simple fallback item rather than sending to NLP.
        if not text_to_process:
            parsed_ingredients.append({
                "quantity": "", "unit": "",
                "name": original_full_line.strip(), "display_text": original_full_line.strip()
            })
            continue

        texts_for_nlp_pipe_with_context.append((line, text_to_process, is_garnish_header_line, i))
        nlp_input_texts.append(text_to_process)


    # Process all collected texts in a batch using nlp.pipe
    # batch_size can be adjusted for performance, typically 50-100 or more.
    # n_process can be set to the number of CPU cores for parallel processing, if applicable.
    # For smaller models or few lines, n_process=1 (default) might be faster due to multiprocessing overhead.
    docs_generator = nlp_model.pipe(nlp_input_texts, batch_size=64, n_process=1) # n_process=1 often best for custom NER unless CPU bound

    # Now, iterate through the original context and the processed docs
    # Ensure a 1:1 mapping between nlp_input_texts and docs_generator
    results_map = {} # To store results and sort by original index later if input lines were split
    for (original_full_line, text_used_for_nlp, is_garnish_header_line, original_index), doc in zip(texts_for_nlp_pipe_with_context, docs_generator):
        parsed_item = format_extracted_entities(doc, text_used_for_nlp) # Pass text_used_for_nlp as original_text to format_extracted_entities

        if parsed_item:
            # For garnish lines, the display_text should be the full original line,
            # even if the parsing only happened on the part after the colon.
            if is_garnish_header_line:
                parsed_item["display_text"] = original_full_line.strip()
            else:
                # If it's not a garnish header, display_text from format_extracted_entities is correct
                # (it uses text_used_for_nlp internally, which is correct here)
                pass
            results_map[original_index] = parsed_item
        else:
            # Fallback if parsing fails, add as a basic item with only desired fields
            results_map[original_index] = {
                "quantity": "",
                "unit": "",
                "name": original_full_line.strip(), # Use the full original line for fallback name/display
                "display_text": original_full_line.strip()
            }

    # Reconstruct the final list in original order
    for i in range(len(ingredients_list_raw)):
        if i in results_map:
            parsed_ingredients.append(results_map[i])
        # Note: Lines entirely skipped (e.g., "instructions:") will not have an entry in results_map
        # This is desired behavior if those lines should not appear in the parsed output at all.

    return parsed_ingredients

if __name__ == '__main__':
    print("--- Benchmarking ingredient_parser.py (NLP Pipe) ---")

    # Create a larger list for a more noticeable benchmark
    sample_ingredients = [
        "1/2 cup finely chopped pecans, for garnish",
        "2 large eggs",
        "salt",
        "1 tbsp fresh parsley, chopped (or dried)",
        "300g chicken breast, sliced",
        "1 (15-ounce) can black beans, rinsed and drained",
        "Juice of 2 lemons (about 1/4 cup)",
        "1 large onion, chopped",
        "2 tablespoons olive oil",
        "1 (15-ounce) can crushed tomatoes",
        "1/2 teaspoon dried oregano, or to taste",
        "Salt and freshly ground black pepper, to taste",
        "4 ounces pasta, such as spaghetti (about 1 cup cooked)",
        "For the garnish: chopped fresh parsley",
        "1 chicken breast, skin removed and cut into bite-sized pieces",
        "mediumtolarge sweet potato, peeled and diced",
        "2-ounce bar unsweetened chocolate, chopped",
        "1 whole chicken (about 3 pounds), cut into 8 pieces",
        "1 large bell pepper (any color), sliced",
        "a pinch of cayenne pepper",
        "water", # Short, no entities
        "Instructions: Preheat oven to 350F.", # Should be skipped
        "Notes: Serve warm." # Should be skipped
    ]

    # Generate a very large list to clearly see batching benefits
    num_repetitions = 1000 # Increase this for more significant benchmarks
    large_test_ingredients = []
    for _ in range(num_repetitions):
        large_test_ingredients.extend(sample_ingredients)
    print(f"Total lines to process: {len(large_test_ingredients)}")

    start_time = time.time()
    parsed_large_set = extract_ingredients_ner(large_test_ingredients)
    end_time = time.time()
    print(f"\nProcessing {len(large_test_ingredients)} lines took: {end_time - start_time:.4f} seconds")

    # Print a few examples from the large set to confirm output format
    print("\nSample from Parsed Large Set (first 3):")
    for item in parsed_large_set[:3]:
        print(item)
    print("\nSample from Parsed Large Set (last 3):")
    for item in parsed_large_set[-3:]:
        print(item)

    print("\n--- Original Test Cases (still running) ---")
    parsed_sample_set = extract_ingredients_ner(sample_ingredients)
    print("\nParsed Sample Set:")
    for item in parsed_sample_set:
        print(item)
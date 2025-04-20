import re
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc # Import Doc

# Load spacy model (ensure it's loaded only once if possible, e.g., via fixture or module scope)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# Define common units (Copied from user code)
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
    "each", "large", "medium", "small", "can", "cans", "stick", "sticks", "bag", "bags",
    # Added from tests
    "clove", "cloves", "pinch", "pinches", "package", "packages", "slice", "slices",
    "bunch", "bunches", "head", "heads",
}
QUANTIY_ERRORS = ['ice'] # Ingredients where quantity parsing is often wrong

# Word-to-number mapping (Copied from user code)
WORD_NUMBERS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "half": 0.5, "quarter": 0.25,
    "a": 1, "an": 1, # Added 'a'/'an'
}

# Known preparation/instruction words/phrases to remove
# Added more descriptive words and refined regex matching
PREP_WORDS = {
    # Actions/Verbs (often participle adjectives)
    'melted', 'cooled', 'softened', 'chilled', 'frozen', 'heated', 'warmed',
    'chopped', 'sliced', 'diced', 'minced', 'grated', 'shredded', 'peeled', 'zested',
    'juiced', 'seeded', 'pitted', 'cored', 'trimmed', 'halved', 'quartered', 'cut',
    'beaten', 'broken', 'whisked', 'mashed', 'crushed', 'ground', 'toasted', 'roasted',
    'cooked', 'uncooked', 'boiled', 'steamed', 'fried', 'baked', 'grilled',
    'rinsed', 'drained', 'packed', 'sifted', 'divided', 'removed', 'discarded',
    'reserved',

    # Descriptors/Adverbs/Adjectives (often removable)
    'optional', 'plus', 'more', 'additional', 'extra',
    'thinly', 'finely', 'roughly', 'coarsely', # Adverbs modifying prep words
    # 'freshly', # Keep 'freshly ground' for now
    'lightly', 'slightly',
    'large', 'medium', 'small', 'thin', 'thick', # Sizes often removable unless key - handle carefully
    'fresh', 'dried', 'canned', 'frozen', 'raw', # States often removable, handle carefully ('dried basil' vs 'basil')

    # Phrases/Prepositions often indicating instructions (handled better by SUFFIX_PHRASES)
    # 'at', 'room', 'temperature', # Covered by SUFFIX_PHRASES
    # 'for', 'garnish', 'serving', 'brushing', 'drizzling', 'dusting', # Covered by SUFFIX_PHRASES
    # 'into', 'pieces', 'cubes', 'strips', 'wedges', # Covered by SUFFIX_PHRASES
    'to', 'taste', # Specific phrase handled below

    # Other potentially noisy words
    'preferably', 'about', 'approximately', 'such', 'as', 'well',
}
# Regex to remove prep words/phrases, especially from the end or after commas
# Look for comma or space, then sequence of prep words/related punctuation near the end
# This is tricky. Let's simplify: Remove known suffix words if they appear after the core noun phrase.
PREP_SUFFIX_REGEX = re.compile(
    # Optional comma/space + known word + optional following words until end or another core word
    r'(?:,\s*|\s+)(' + '|'.join(re.escape(s) for s in PREP_WORDS) + r')(\b.*)?$',
    re.IGNORECASE
)

# Descriptive adjectives to potentially remove if leading and not essential
LEADING_DESCRIPTIVE_ADJ = {'large', 'medium', 'small', 'fresh', 'dried', 'thin', 'thick'}
# IMPORTANT_FOOD_ADJECTIVES = {
#     'navy', 'black', 'white', 'red', 'green', 'yellow', 'brown', 'purple',
#     'sweet', 'sour', 'spicy', 'hot', 'mild', 'baking', 'dried', 'fresh',
#     'ground', 'whole', 'skim', 'low-fat', 'nonfat', 'full-fat', 'fat-free',
#     'wild', 'farm-raised', 'organic', 'conventional', 'raw', 'cooked',
#     'italian', 'french', 'chinese', 'japanese', 'mexican', 'greek', 'thai',
#     'extra-virgin', 'virgin', 'light', 'dark', 'sea', 'kosher', 'iodized',
#     'unsalted', 'salted', 'roasted', 'toasted', 'smoked', 'canned',
#     'frozen', 'crunchy', 'creamy', 'smooth', 'chunky', 'baby', 'condensed',
#     'evaporated', 'unsweetened'
# }
# --- SUFFIX_PHRASES: Known phrases to remove reliably from the end ---

SUFFIX_PHRASES = [
    r'at room temperature',
    r'room temperature',
    r'plus more for .*', # e.g., plus more for brushing
    r'plus more',
    r'melted and cooled', # Order matters, longer first
    r'melted cooled',
    r'to taste',
    r'for garnish',
    r'for serving',
    r'for brushing',
    r'optional',
    r'divided',
    r'such as .*?', # non-greedy
    r'preferably .*?', # non-greedy
    r'cut into .*',
    r'rinsed and drained',
    r'peeled and (?:diced|chopped|sliced|minced)',
    r'seeded and (?:diced|chopped|sliced|minced)',
    r',? or more',
    r'or more',
    r'as needed',
    r'if desired',
    r'melted', # Single words if they weren't caught by PREP_WORDS token removal
    r'cooled',
    r'chopped',
    r'diced',
    r'sliced',
    r'minced',
    r'peeled',
    r'seeded',
    r'rinsed',
    r'drained',
    r'beaten',
    r'pitted',
    r'softened',
    r'undrained'
]
# Compile suffix regex (match optional comma/space + phrase at the end)
SUFFIX_REGEX = re.compile(
    # Optional leading comma or whitespace (zero or more)
    r'[,\s]*(?:' +
    # Non-capturing group of all alternatives from the list
    '|'.join(SUFFIX_PHRASES) +
    # End of string anchor
    r')$',
    re.IGNORECASE
)
# Converts a fraction string to float (Copied from user code)
def parse_fraction(s):
    s = s.strip()
    try:
        if ' ' in s: # Mixed number like "1 1/2"
            parts = s.split()
            if len(parts) == 2 and '/' in parts[1]:
                whole, frac = parts
                num, denom = frac.split('/')
                return float(whole) + float(num) / float(denom)
            else: # Could be range "1 2" or just number "1 ", try float directly
                return float(parts[0])
        elif '/' in s:
            num, denom = s.split('/')
            return float(num) / float(denom)
        else:
            return float(s)
    except ValueError: # Handle non-numeric directly
        return None
    except ZeroDivisionError:
        return None


def handle_or_pattern(text):
    """
    For ingredients with 'or' pattern, extract the first ingredient.
    E.g., 'swiss chard or mustard greens' -> 'swiss chard'
    """
    if not text:
        return text

    # Check for 'or' not within parentheses
    if ' or ' in text and not re.search(r'\([^)]*or[^)]*\)', text):
        parts = text.split(' or ')
        if parts[0].strip():
            return parts[0].strip()

    return text

def extract_core_name_spacy(full_name_text: str) -> str:
    """
    Extracts the core ingredient name using spaCy, applying suffix phrase removal
    first, then noun chunking, and finally token-level trimming.
    """
    if not isinstance(full_name_text, str) or not full_name_text.strip():
        return ""
    full_name_text = handle_or_pattern(full_name_text)

    # --- 1. Pre-processing ---
    # Remove content in parentheses first
    text = re.sub(r'\([^)]*\)', '', full_name_text)
    # Normalize hyphens and strip whitespace
    text = text.replace(' - ', '-').strip()
    if not text: return ""
    original_input_after_paren_removal = text # Keep for fallback

    # --- 2. Iterative Suffix Phrase Removal ---
    # Apply the suffix regex repeatedly to the current string
    core_name = text
    iterations = 0
    max_iterations = len(SUFFIX_PHRASES) + 2 # Safety break
    while iterations < max_iterations:
        # Apply the regex
        new_name = SUFFIX_REGEX.sub('', core_name).strip()
        # Remove any trailing comma left after substitution
        if new_name.endswith(','):
            new_name = new_name[:-1].strip()

        # Check if anything changed
        if new_name == core_name:
            break # No change, exit loop

        core_name = new_name
        # Break if the string becomes empty
        if not core_name:
            break
        iterations += 1

    # --- 3. Fallback if Suffix Removal Emptied String ---
    # If core_name is empty now, revert to the state before suffix removal
    # if not core_name:
    #     core_name = original_input_after_paren_removal
    #     # If the original was also effectively empty, return ""
    #     if not core_name.strip(): return ""

    # --- 4. SpaCy Processing on Cleaned Text ---
    # Process the text *after* major suffix phrases have been removed
    doc = nlp(core_name)
    candidate_span = None

    # --- 5. Identify Core Noun Phrase using Noun Chunks ---
    noun_chunks = list(doc.noun_chunks)

    if noun_chunks:
        # Heuristic: Start with the last noun chunk that doesn't seem like just prep words
        for chunk in reversed(noun_chunks):
            is_likely_prep_only = True
            # Check if chunk contains at least one noun/propn not in prep words
            for token in chunk:
                if token.pos_ in ['NOUN', 'PROPN'] and token.lemma_.lower() not in PREP_WORDS:
                    is_likely_prep_only = False
                    break
                # Allow adjectives NOT in prep words too (e.g., 'black' in 'black pepper')
                elif token.pos_ == 'ADJ' and token.lemma_.lower() not in PREP_WORDS:
                    is_likely_prep_only = False
                    break
                if not is_likely_prep_only:
                    candidate_span = chunk
                    break # Found a potential core chunk
            starts_with_prep_verb = False
            if chunk.text.split()[0].lower() in ["removed", "chopped", "sliced", "diced", "minced"]:
                starts_with_prep_verb = True

            if not is_likely_prep_only and not starts_with_prep_verb:
                candidate_span = chunk
                break  # Take the first valid chunk and break

        # If a candidate was found, try extending backwards for conjunctions ('and')
        if candidate_span:
            if candidate_span.start > 0:
                prev_token = doc[candidate_span.start - 1]
                # If 'and' connects to a preceding Noun/Propn
                if prev_token.lemma_ == 'and' and prev_token.i > 0:
                    token_before_and = doc[prev_token.i - 1]
                    if token_before_and.pos_ in ['NOUN', 'PROPN', 'ADJ']: # Adj like 'black and white pepper'
                        # Find the noun chunk ending right before 'and'
                        for prev_chunk in reversed(noun_chunks):
                            if prev_chunk.end == prev_token.i:
                                # Combine the spans
                                candidate_span = doc[prev_chunk.start : candidate_span.end]
                                break
        else:
            # If no suitable chunk found, use the whole doc as the candidate
            candidate_span = doc[:]

    else:
        # No noun chunks found at all, use the whole doc
        candidate_span = doc[:]

    # If candidate_span is somehow None or empty, fallback
    if not candidate_span or not candidate_span.text.strip():
        # Fallback to the text after suffix removal, before chunking attempt
        core_name = doc.text.strip()
        if not core_name: return "" # Return empty if everything failed
    else:
        core_name = candidate_span.text.strip()


    # --- 6. Token-based Prefix/Suffix Trimming using PREP_WORDS ---
    # Apply to the 'core_name' identified from chunks/suffixes
    if not core_name: return "" # Exit if empty before trimming

    temp_doc = nlp(core_name) # Re-process the refined core_name for accurate tokens
    start_token_idx = 0
    end_token_idx = len(temp_doc)

    # Trim Prefixes
    for i, token in enumerate(temp_doc):
        token_lemma_lower = token.lemma_.lower()
        # Condition: Is a prep word AND is ADV/ADJ/VERB/PART (typical modifier POS tags)
        if token_lemma_lower in PREP_WORDS and token.pos_ in ['ADV', 'ADJ', 'VERB', 'PART']:
            # Protect essential adjectives if necessary by curating PREP_WORDS carefully
            # Stop trimming if this is the last token or followed by hyphen
            if i < len(temp_doc) - 1 and temp_doc[i+1].text != '-':
                start_token_idx = i + 1
            else: break # Don't trim the only word or word before hyphen
        # Stop if it's a noun/propn (even if in prep words - e.g. 'ground') or not a prep word
        elif token_lemma_lower not in PREP_WORDS or token.pos_ in ['NOUN', 'PROPN']:
            break
        # Stop also for other non-modifier POS tags
        elif token.pos_ not in ['ADV', 'ADJ', 'VERB', 'PART']:
            break

    # Trim Suffixes (go backwards from end towards start_token_idx)
    for i in range(len(temp_doc) - 1, start_token_idx - 1, -1):
        token = temp_doc[i]
        token_lemma_lower = token.lemma_.lower()
        # Condition: Is a prep word AND is ADV/ADJ/VERB/PART/ADP (allow trailing preps like 'for')
        if token_lemma_lower in PREP_WORDS and token.pos_ in ['ADV', 'ADJ', 'VERB', 'PART', 'ADP']:
            if i > start_token_idx: # Ensure we don't trim the only remaining token
                end_token_idx = i # Set new end boundary (exclusive)
            else: break # Stop if it's the only token left
        # Also remove trailing punctuation
        elif token.is_punct and i >= start_token_idx:
            end_token_idx = i
        # Stop if it's a noun/propn or not a prep word
        elif token_lemma_lower not in PREP_WORDS or token.pos_ in ['NOUN', 'PROPN']:
            break
        # Stop also for other non-modifier POS tags from the end
        elif token.pos_ not in ['ADV', 'ADJ', 'VERB', 'PART', 'ADP', 'PUNCT']:
            break


    # --- 7. Final Name Construction and Cleanup ---
    final_name = ""
    if start_token_idx < end_token_idx:
        # Extract the final span based on trimming indices
        final_name = temp_doc[start_token_idx:end_token_idx].text.strip()

    # If trimming resulted in empty string, fallback to name before trimming
    if not final_name:
        final_name = core_name # Use the name identified after suffix removal/chunking

    # Final cleanup: residual hyphens, multiple spaces
    final_name = final_name.replace(' - ', '-')
    final_name = ' '.join(final_name.split())

    # Last check: if somehow empty, fallback to original input after parens removed
    if not final_name:
        return original_input_after_paren_removal

    return final_name
# ========================================
# Rest of your xtractServer code (extract_ingredients)
# Needs to be updated to USE the refined extract_core_name_spacy
# Make sure imports are correct if this is in a different file.
# ========================================

# Example of how extract_ingredients might use it (simplified)
# Assume extract_core_name_spacy is imported correctly
# aking changes to the juice/zest/peel pattern handling in extract_ingredients function
def extract_ingredients(text):
    ingredients = []
    # First split on semicolons and newlines
    initial_lines = [line.strip() for line in re.split(r'[;\n]|,(?![^\(]*\))', text) if line.strip()]

    # Process each line and check for valid "and" to split ingredients
    lines = []
    for line in initial_lines:
        # Skip splitting common combined seasonings and fixed phrases
        if re.search(r'salt\s+and\s+pepper.', line, re.IGNORECASE) or \
                re.search(r'oil\s+and\s+vinegar', line, re.IGNORECASE) or \
                re.search(r'macaroni\s+and\s+cheese', line, re.IGNORECASE) or \
                re.search(r'peanut\s+butter\s+and\s+jelly', line, re.IGNORECASE):
            lines.append(line)
        elif " and " in line and not re.search(r'\([^)]*and[^)]*\)', line):
            # Make sure "and" is not in parentheses
            parts = line.split(" and ")
            for part in parts:
                if part.strip():  # Ensure non-empty
                    lines.append(part.strip())
        else:
            lines.append(line)

    for line in lines:
        original_line = line
        display_text = original_line.lower()  # Standardize display text to lower

        # --- Pre-checks for section headers / instructions ---
        if re.match(r'^(?:For the .*?:|Instructions:|Notes:|Optional:|Serving Suggestions:|Garnish:|Equipment:)', line, re.IGNORECASE):
            # Try to extract item after colon if it's a specific garnish/suggestion
            match = re.search(r':\s*(.+)', line)
            if match:
                name_part = match.group(1).strip()
                core_name = extract_core_name_spacy(name_part)  # Use the function here
                if core_name:
                    ingredients.append({
                        "name": core_name.lower(),
                        "display_text": display_text,
                        "quantity": "",  # Often no quantity for garnish section titles
                    })
            continue  # Skip parsing this line as a standard ingredient

        # --- Parsing Logic ---
        doc = nlp(line)
        quantity = ""
        unit = ""
        name_part = line  # Start with the full line

        # 1. Find Quantity and Unit at the beginning
        qty_parts = []
        unit_candidate = ""
        potential_name_start_index = 0

        for i, token in enumerate(doc):
            token_text_lower = token.text.lower()
            # Check for numbers (digits, fractions, words)
            is_number_word = token_text_lower in WORD_NUMBERS
            is_numeric = token.like_num or '/' in token.text

            if is_numeric or is_number_word:
                qty_parts.append(token.text)
                potential_name_start_index = token.i + 1
            # Check for unit immediately after quantity parts
            elif qty_parts and token_text_lower in UNITS:
                # Check if previous token was indeed part of quantity
                if token.i == potential_name_start_index:
                    unit_candidate = token_text_lower
                    potential_name_start_index = token.i + 1
                else:  # Word after quantity isn't a unit, likely start of name
                    break
            # Handle "a pinch", "a clove" - where 'a' is quantity 1
            elif token_text_lower in ['a', 'an'] and i == 0 and i + 1 < len(doc) and doc[i+1].lemma_.lower() in UNITS:
                qty_parts.append("1")
                unit_candidate = doc[i+1].lemma_.lower()
                potential_name_start_index = i + 2
                break  # Found qty and unit
            # Handle "to taste" - no quantity/unit
            elif token_text_lower == 'to' and i + 1 < len(doc) and doc[i+1].lemma_ == 'taste':
                potential_name_start_index = 0  # The whole phrase is the name
                qty_parts = []  # Reset quantity
                break
            # Stop searching for quantity/unit if we hit a non-qty/non-unit word after finding some quantity
            # or if we hit a clear name part (Noun/Propn not in units)
            elif token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and token_text_lower not in UNITS:
                if qty_parts:  # Found name part after quantity
                    break
                else:  # Found name part before any quantity (e.g., "Salt")
                    potential_name_start_index = i
                    break
            # Stop if we hit the end or punctuation generally
            elif token.is_punct and token.text != '/':  # Allow '/' for fractions
                if qty_parts: break  # Stop after quantity if punctuation hit
                else: potential_name_start_index = i+1  # Punctuation before name start
            # Allow adjectives between quantity and unit/name? (e.g., "1 large egg")
            elif token.pos_ == 'ADJ' and qty_parts:
                # If the *next* token is a unit, treat this ADJ as a unit
                if i + 1 < len(doc) and doc[i+1].text.lower() in UNITS:
                    unit_candidate = token.text.lower()  # e.g. 'large'
                    potential_name_start_index = i + 1
                # Otherwise, assume it's start of name
                else:
                    break
            elif qty_parts:  # Found something else after qty parts, assume name starts
                break
            else:  # Haven't found quantity yet, continue scan
                potential_name_start_index = i + 1

        # Process collected quantity parts
        if qty_parts:
            quantity_str = " ".join(qty_parts)
            # Try parsing quantity (handles fractions, words etc.)
            parsed_qty_val = parse_fraction(quantity_str)
            if parsed_qty_val is not None:
                # Format to avoid unnecessary decimals for integers
                quantity = str(int(parsed_qty_val)) if parsed_qty_val == int(parsed_qty_val) else f"{parsed_qty_val:.2f}".rstrip('0').rstrip('.')  # Format nicely
            else:
                # Could be a word quantity we didn't parse, or something else.
                # If it was a word number, handle it
                word_val = WORD_NUMBERS.get(quantity_str.lower())
                if word_val is not None:
                    quantity = str(word_val)
                else:
                    # Failed to parse, maybe it wasn't quantity? Reset.
                    quantity = ""
                    potential_name_start_index = 0  # Assume name starts from beginning
                    unit_candidate = ""  # Reset unit too

        # Assign unit if found
        if unit_candidate:
            unit = unit_candidate

        # Extract name part from the rest of the line
        name_part = doc[potential_name_start_index:].text.strip()

        # 2. Check for "juice of X" pattern BEFORE extracting core name
        juice_match = re.match(r'(?i)^(juice|zest|peel)\s+of\s+(.*)', name_part)
        has_juice_pattern = False

        if juice_match:
            has_juice_pattern = True
            prep_type = juice_match.group(1).lower()
            rest = juice_match.group(2).strip()

            # Try to find the item name ("lemon", "orange")
            item_doc = nlp(rest)
            item_name = ""
            for token in item_doc:
                if token.pos_ in ['NOUN', 'PROPN']:
                    item_name = token.lemma_  # Use lemma for singular form
                    break

            if item_name:
                # Correctly format as "lemon juice" instead of "juice lemon"
                core_name = f"{item_name} {prep_type}"
                # Quantity might be in rest, e.g., "2 lemons" - handled by initial parse?
                # If quantity wasn't found initially, try to extract from the rest
                if not quantity:
                    # Look for numbers in the rest part
                    for token in item_doc:
                        if token.like_num or token.text.lower() in WORD_NUMBERS:
                            if token.like_num:
                                quantity = token.text
                            else:
                                quantity = str(WORD_NUMBERS[token.text.lower()])
                            break
                    # If still no quantity, default to 1
                    if not quantity:
                        quantity = "1"

                # If unit wasn't found, use the item name as unit (e.g., "1 lemon")
                if not unit:
                    unit = item_name

        # Only extract core name if we didn't handle a juice pattern
        if not has_juice_pattern:
            # Extract Core Name using the refined function
            core_name = extract_core_name_spacy(name_part)

        # 3. Handle special cases / Refinements
        # Handle parentheses with quantity and unit info
        paren_match = re.search(r'\((?:about|approx\.?|yields?)\s*([\d\s./]+)\s*(\w+)\s*\)', name_part, re.IGNORECASE)

        # Prefer quantity/unit from parentheses if available and standard
        if paren_match:
            paren_qty_str = paren_match.group(1).strip()
            paren_unit = paren_match.group(2).strip().lower()
            parsed_paren_qty = parse_fraction(paren_qty_str)

            if parsed_paren_qty is not None and paren_unit in UNITS:
                paren_quantity = str(int(parsed_paren_qty)) if parsed_paren_qty == int(parsed_paren_qty) else f"{parsed_paren_qty:.2f}".rstrip('0').rstrip('.')
                # Overwrite if parenthesis provides standard unit/qty
                quantity = paren_quantity
                unit = paren_unit

        # Handle "salt and pepper to taste"
        if "to taste" in name_part.lower() and not quantity:
            core_name = extract_core_name_spacy(name_part.lower().replace("to taste", "").strip())
            quantity = ""  # Explicitly empty
            unit = ""

        # --- Final Assembly ---
        # Only add if a core name was identified
        if core_name:
            ingredient = {
                "name": core_name.lower(),
                "display_text": display_text,  # Use original line, lowercased
                "quantity": quantity.strip(),
            }
            # Add unit only if it exists
            if unit:
                ingredient["unit"] = unit.lower().strip()

            ingredients.append(ingredient)
        elif line and not re.match(r'^\s*$', line):  # Log lines that didn't parse to anything useful
            # Maybe add it with just display_text? Or log?
            print(f"Skipping line - no core ingredient name found: '{line}' -> Name Part: '{name_part}' -> Core Name: '{core_name}'")

    return ingredients
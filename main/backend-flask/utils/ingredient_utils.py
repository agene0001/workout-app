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
    'lengthwise',
    'undrained','melted', 'cooled', 'softened', 'chilled', 'frozen', 'heated', 'warmed',
    'chopped', 'sliced', 'diced', 'minced', 'grated', 'shredded', 'peeled', 'zested',
    'juiced', 'seeded', 'pitted', 'cored', 'trimmed', 'halved', 'quartered', 'cut',
    'beaten', 'broken', 'whisked', 'mashed', 'crushed', 'ground', 'toasted', 'roasted',
    'cooked', 'uncooked', 'boiled', 'steamed', 'fried', 'baked', 'grilled',
    'rinsed', 'drained', 'packed', 'sifted', 'divided', 'removed', 'discarded',
    'reserved',

    # Descriptors/Adverbs/Adjectives (often removable)
    'optional', 'plus', 'more', 'additional', 'extra',
    'thinly', 'finely', 'roughly', 'coarsely', # Adverbs modifying prep words
    'freshly', # Keep 'freshly ground' for now
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
    r'undrained',
    r'lengthwise',
    r'quartered',
    r'cleaned',
    r'de-bearded',
    r'deveined'
    r'stems removed'
    # r'freshly'
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
def preprocess_hyphenated_units(text, units_set):
    """
    Finds patterns like 'NUMBER-UNIT' (e.g., '15-ounce') where UNIT is known,
    and merges them into 'NUMBERUNIT' (e.g., '15ounce') to help tokenization.
    """
    def replacer(match):
        number_part = match.group(1)
        unit_part = match.group(2)
        # Check if the part after hyphen is a known unit
        if unit_part.lower() in units_set:
            # Merge them without hyphen
            return f"{number_part}{unit_part}"
        else:
            # Not a known unit, leave it as is
            return match.group(0)

    # Regex: digits/dots/slashes, hyphen, word characters
    pattern = re.compile(r'(\d[\d./]*)-(\w+)')
    return pattern.sub(replacer, text)
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
    core_name = suffix_removal(text)

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
            if chunk.text.split()[0].lower() in PREP_WORDS:
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

def suffix_removal(word):
    iterations = 0
    max_iterations = len(SUFFIX_PHRASES) + 5 # Safety
    cleaned_line = word.strip()
    while iterations < max_iterations:
        new_cleaned_line = SUFFIX_REGEX.sub('', cleaned_line).strip()
        # Remove any trailing comma left after substitution
        if new_cleaned_line.endswith(','):
            new_cleaned_line = new_cleaned_line[:-1].strip()

        # Check if anything changed
        if new_cleaned_line == cleaned_line:
            break # No change, exit loop

        cleaned_line = new_cleaned_line
        # Break if the string becomes empty
        if not cleaned_line:
            break
        iterations += 1
    return cleaned_line
# ========================================
# Rest of your xtractServer code (extract_ingredients)
# Needs to be updated to USE the refined extract_core_name_spacy
# Make sure imports are correct if this is in a different file.
# ========================================

# Example of how extract_ingredients might use it (simplified)
# Assume extract_core_name_spacy is imported correctly
# aking changes to the juice/zest/peel pattern handling in extract_ingredients function
def extract_ingredients(ingredients_list):
    extracted_data =[]

    # Process each line and check for valid "and" to split ingredients
    lines = []
    for line in ingredients_list:
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
        # display_text = original_line.lower()  # Standardize display text to lower
        suffix_removed = suffix_removal(original_line)
        preprocessed_text = preprocess_hyphenated_units(suffix_removed, UNITS)
        display_text = suffix_removed.lower()
        # --- Pre-checks for section headers / instructions ---
        if re.match(r'^(?:For the .*?:|Instructions:|Notes:|Optional:|Serving Suggestions:|Garnish:|Equipment:)', line, re.IGNORECASE):
            # Try to extract item after colon if it's a specific garnish/suggestion
            match = re.search(r':\s*(.+)', line)
            if match:
                name_part = match.group(1).strip()
                core_name = extract_core_name_spacy(name_part)  # Use the function here
                if core_name:
                    extracted_data.append({
                        "name": core_name.lower(),
                        "display_text": display_text,
                        "quantity": "",  # Often no quantity for garnish section titles
                    })
            continue  # Skip parsing this line as a standard ingredient

        # --- Parsing Logic ---
        # --- Parsing Logic ---
        doc = nlp(preprocessed_text) # Ensure using cleaned text
        # print(f"\n--- PARSING ---")             # <<< DEBUGGING LINE
        # print(f"DEBUG: Input to NLP: '{doc.text}'") # <<< DEBUGGING LINE
        # print(f"DEBUG: Tokens: {[t.text for t in doc]}") # <<< DEBUGGING LINE

        quantity = ""
        unit = ""
        potential_name_start_index = 0
        qty_parts = []
        unit_candidate = "" # Ensure reset

        # 1. Find Quantity and Unit
        i = 0
        # --- WHILE LOOP BLOCK TO REPLACE/INSERT ---
        while i < len(doc):
            token = doc[i]
            token_text = token.text
            token_text_lower = token_text.lower()
            is_number_word = token_text_lower in WORD_NUMBERS
            # Strict check: '-' not allowed in quantity parts unless it's a fraction like 1/2
            is_numeric_strict = (token.like_num or '/' in token_text) and '-' not in token_text[1:] # Allow leading '-' ?

            # --- Step 1: Accumulate Quantity ---
            if (is_numeric_strict or is_number_word) and not unit_candidate and i == potential_name_start_index:
                qty_parts.append(token_text)
                potential_name_start_index = i + 1
                i += 1
                continue

            # --- Step 2: Evaluate token immediately after quantity stops ---
            elif qty_parts and i == potential_name_start_index:
                current_token_is_unit = token_text_lower in UNITS
                next_token_exists = i + 1 < len(doc)
                next_token_is_unit = next_token_exists and doc[i+1].text.lower() in UNITS

                # CASE 2a: Current token is the unit
                if current_token_is_unit:
                    unit_candidate = token_text_lower
                    potential_name_start_index = i + 1
                    if next_token_is_unit: i += 1; continue # Compound unit check
                    else: break # Unit found

                # CASE 2b: Current token NOT unit, BUT NEXT IS unit (QTY DESC UNIT)
                elif next_token_is_unit:
                    unit_candidate = doc[i+1].text.lower() # Unit is NEXT token
                    potential_name_start_index = i + 2     # Name starts after unit
                    break # Unit found

                # CASE 2c: Neither current nor next is unit -> Name starts here
                else: break # Name identified, current token is start of name

            # --- Step 3: Handle second part of compound unit ---
            elif unit_candidate and i == potential_name_start_index:
                if token_text_lower in UNITS:
                    unit_candidate += " " + token_text_lower
                    potential_name_start_index = i + 1
                break # Stop after checking for second unit part

            # --- Step 4: Handle starting "a/an" ---
            elif token_text_lower in ['a', 'an'] and i == 0 and not qty_parts:
                if i + 1 < len(doc) and doc[i+1].lemma_.lower() in UNITS:
                    qty_parts.append("1")
                    unit_candidate = doc[i+1].lemma_.lower()
                    potential_name_start_index = i + 2
                else: potential_name_start_index = i # Name starts at 'a'/'an'
                break # Exit after handling 'a'/'an'

            # --- Step 5: Loop termination condition ---
            else:
                if not qty_parts: potential_name_start_index = i # No qty found
                break # Exit loop
        # --- END OF WHILE LOOP BLOCK ---

        # print(f"DEBUG: Loop finished. Qty='{qty_parts}', UnitCand='{unit_candidate}', NameIdx={potential_name_start_index}") # <<< DEBUGGING LINE

        # Process collected quantity parts
        if qty_parts:
            quantity_str = " ".join(qty_parts)
            parsed_qty_val = parse_fraction(quantity_str)
            if parsed_qty_val is not None:
                quantity = str(int(parsed_qty_val)) if parsed_qty_val == int(parsed_qty_val) else f"{parsed_qty_val:.3f}".rstrip('0').rstrip('.')
            else:
                word_val = WORD_NUMBERS.get(quantity_str.lower())
                if word_val is not None: quantity = str(word_val)
                else: quantity = ""; potential_name_start_index = 0; unit_candidate = "" # Reset

        # Assign unit IF FOUND
        # --- MODIFIED UNIT ASSIGNMENT WITH DEBUG ---
        if unit_candidate: # Check if unit_candidate has a non-empty value
            unit = unit_candidate
            # print(f"DEBUG: Assigned unit = '{unit}' (from unit_candidate = '{unit_candidate}')") # <<< DEBUGGING LINE
        else:
            unit = "" # Explicitly set to empty if no candidate
            # print(f"DEBUG: No unit assigned (unit_candidate was '{unit_candidate}')")       # <<< DEBUGGING LINE

        # Extract name part
        if not quantity and not unit and potential_name_start_index != 0 and not qty_parts:
            potential_name_start_index = 0

        # Ensure name_part is derived from the correct doc and index
        # Check bounds before slicing
        if potential_name_start_index < len(doc):
            name_part = doc[potential_name_start_index:].text.strip()
        else:
            name_part = "" # Handle index out of bounds
        # print(f"DEBUG: Derived name_part = '{name_part}' (from index {potential_name_start_index})") # <<< DEBUGGING LINE

        # Check for Juice Pattern
        # ... (juice logic remains the same) ...
        has_juice_pattern = False
        core_name = ""
        juice_match = re.match(r'(?i)^(juice|zest|peel)\s+of\s+(.*)', name_part)
        if juice_match:
            # ... (juice logic - ensure core_name is assigned here) ...
            has_juice_pattern = True
            prep_type = juice_match.group(1).lower()
            rest = juice_match.group(2).strip()
            item_doc = nlp(rest)
            item_name = ""
            for token_j in item_doc: # Use different loop variable
                if token_j.pos_ in ['NOUN', 'PROPN']: item_name = token_j.lemma_; break
            if item_name: core_name = f"{item_name} {prep_type}"
            # ... quantity/unit override for juice ...
            if not quantity:
                for token_j in item_doc:
                    if token_j.like_num or token_j.text.lower() in WORD_NUMBERS:
                        if token_j.like_num: quantity = token_j.text
                        else: quantity = str(WORD_NUMBERS[token_j.text.lower()])
                        break
                if not quantity: quantity = "1"
            if not unit: unit = item_name # Override unit only if not found earlier

        # Extract core name if not juice pattern
        if not has_juice_pattern and name_part: # Ensure name_part is not empty
            core_name = extract_core_name_spacy(name_part)
        elif not name_part:
            core_name = "" # Ensure core_name is empty if name_part was empty

        # print(f"DEBUG: Core name = '{core_name}' (from name_part = '{name_part}')") # <<< DEBUGGING LINE


        # Handle Parentheses (Check suffix_removed string)
        # Important: This could potentially overwrite the unit found by the loop!
        paren_match = re.search(r'\((?:about|approx\.?|yields?|around)\s*([\d\s./]+)\s*(\w+)\s*\)', suffix_removed, re.IGNORECASE) # Added 'around'
        if paren_match:
            # print(f"DEBUG: Found parenthesis match: {paren_match.groups()}") # <<< DEBUGGING LINE
            paren_qty_str = paren_match.group(1).strip()
            paren_unit = paren_match.group(2).strip().lower()
            parsed_paren_qty = parse_fraction(paren_qty_str)
            # Check if the unit found in parentheses is valid
            if parsed_paren_qty is not None and paren_unit in UNITS:
                # print(f"DEBUG: Overwriting quantity/unit from parentheses. Old unit='{unit}'") # <<< DEBUGGING LINE
                paren_quantity = str(int(parsed_paren_qty)) if parsed_paren_qty == int(parsed_paren_qty) else f"{parsed_paren_qty:.2f}".rstrip('0').rstrip('.')
                quantity = paren_quantity
                unit = paren_unit # <<< THIS IS A POTENTIAL OVERWRITE POINT
                # print(f"DEBUG: New quantity='{quantity}', New unit='{unit}'") # <<< DEBUGGING LINE
            else:
                print(f"DEBUG: Parenthesis unit '{paren_unit}' not in UNITS or quantity invalid.") # <<< DEBUGGING LINE


        # Final Assembly
        # print(f"DEBUG: Final check before assembly: Qty='{quantity}', Unit='{unit}', Name='{core_name}'") # <<< DEBUGGING LINE
        if core_name or (quantity and unit): # Add if core name OR both quantity and unit exist
            ingredient = {
                "name": core_name.lower() if core_name else "",
                "display_text": display_text,
                "quantity": quantity.strip(),
            }
            # Add unit only if it exists and is not empty
            if unit: # Check if unit has a non-empty value
                ingredient["unit"] = unit.lower().strip()

            extracted_data.append(ingredient)
            # print(f"DEBUG: Appended ingredient: {ingredient}") # <<< DEBUGGING LINE

    return extracted_data
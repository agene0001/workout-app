import json
import sys
import spacy
import random
from spacy.training.example import Example
from spacy.training.iob_utils import offsets_to_biluo_tags # Import for checking
from pathlib import Path

# --- GPU Configuration ---
# Attempt to use GPU if available, otherwise fallback to CPU
# You can set this to True to require GPU or False to force CPU
spacy.require_gpu() #will raise an error if GPU is not available.
# spacy.prefer_gpu() #will use GPU if available, else CPU.
USE_GPU = True # Set to False to force CPU even if GPU is available for testing

# --- Model training configuration ---
# Path to your manually curated training data JSON file
TRAIN_DATA_JSON_PATH = Path("./train_data.json") # Assumes it's in the same directory as this script
# Path to your Label Studio JSON export (if you also use it)
LABEL_STUDIO_JSON_PATH = Path("./label_studio_export.json")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent # Adjust if script is elsewhere
MODEL_OUTPUT_DIR = PROJECT_ROOT / "models" / "ingredient_ner_model"
N_ITERATIONS = 120 # Number of training iterations
DROPOUT_RATE = 0.35 # Dropout rate for regularization

def load_train_data_from_json(json_path):
    """Loads training data from a JSON file."""
    if not json_path.exists():
        print(f"ERROR: Training data JSON file not found at {json_path}")
        return []
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            train_data_from_json = json.load(f)
            processed_train_data = []
            for item in train_data_from_json:
                if isinstance(item, list) and len(item) == 2:
                    text, annotations_dict = item
                    if isinstance(annotations_dict, dict) and "entities" in annotations_dict:
                        # Ensure entities are tuples: (start, end, label)
                        entities_as_tuples = [tuple(ent) for ent in annotations_dict["entities"] if isinstance(ent, list) and len(ent) == 3]
                        if len(entities_as_tuples) == len(annotations_dict["entities"]): # Check all converted well
                            processed_train_data.append((text, {"entities": entities_as_tuples}))
                        else:
                            print(f"Warning: Some entities in item were malformed and skipped. Item: {text[:50]}...")
                    else:
                        print(f"Warning: Skipping malformed annotation structure in JSON for item: {text[:50]}...")
                else:
                    print(f"Warning: Skipping malformed item in JSON (expected list of 2 elements): {item}")
            print(f"Successfully loaded and processed {len(processed_train_data)} examples from {json_path}")
            return processed_train_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {json_path}: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while loading/processing {json_path}: {e}")
            return []

def convert_label_studio_to_training_data(label_studio_json_path):
    """
    Converts Label Studio JSON export to a common NER training data format.
    Output format: list of [text, {"entities": [(start, end, label), ...]}]
    """
    converted_data = []
    if not label_studio_json_path.exists():
        print(f"Warning: Label Studio JSON file not found at {label_studio_json_path}. Skipping import.")
        return converted_data

    with open(label_studio_json_path, 'r', encoding='utf-8') as f:
        try:
            data_items = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {label_studio_json_path}: {e}")
            return converted_data

    print(f"Loading data from {label_studio_json_path}...")
    for item in data_items: # This assumes data_items is loaded from JSON
        text = item.get('data', {}).get('text')
        if not text: continue

        annotations_list = item.get('annotations', [])
        if annotations_list and isinstance(annotations_list, list) and len(annotations_list) > 0:
            # Assuming we take the first annotation set if multiple exist
            annotation_set = annotations_list[0]
            if 'result' in annotation_set and isinstance(annotation_set['result'], list):
                annotation_results = annotation_set['result']
                entities = []
                for result in annotation_results:
                    if (result.get('type') == 'labels' and
                            'value' in result and isinstance(result['value'], dict)):
                        val = result['value']
                        # Ensure all required keys are present and are of expected types
                        if ('start' in val and isinstance(val['start'], int) and
                                'end' in val and isinstance(val['end'], int) and
                                val.get('labels') and isinstance(val['labels'], list) and val['labels']):

                            # Make sure offsets are valid
                            if 0 <= val['start'] <= val['end'] <= len(text):
                                entities.append( (val['start'], val['end'], val['labels'][0]) ) # Create tuple
                            else:
                                print(f"Warning: Invalid offsets in Label Studio data for text '{text[:50]}...': start={val['start']}, end={val['end']}, len={len(text)}")
                        # else:
                        # print(f"Warning: Malformed 'value' dict in Label Studio result: {val}")
                if entities:
                    converted_data.append((text, {"entities": entities}))
    print(f"Successfully converted {len(converted_data)} items from Label Studio export.")
    return converted_data

# --- check_data_alignment (Keep your robust version) ---
def check_data_alignment(data_to_check, nlp_model, data_source_name="TRAIN_DATA"):
    # ... (Your existing detailed check_data_alignment function) ...
    # Ensure it handles entities as tuples correctly.
    print(f"\n--- Checking {data_source_name} for alignment issues ---")
    misaligned_count = 0
    all_aligned = True
    for i, (text, annotation) in enumerate(data_to_check):
        doc = nlp_model.make_doc(text)
        entities = annotation.get("entities", [])
        if not entities:
            continue
        try:
            # Ensure entities are tuples and sorted by start offset
            current_entities_as_tuples = [tuple(ent) for ent in entities if isinstance(ent, (list, tuple)) and len(ent) == 3]
            if len(current_entities_as_tuples) != len(entities):
                print(f"Warning: Malformed entity structure in example {i} for text '{text[:50]}...'. Original: {entities}")
            sorted_entities = sorted(current_entities_as_tuples, key=lambda x: x[0])
            tags = offsets_to_biluo_tags(doc, sorted_entities)
        except Exception as e:
            print(f"\n--- ERROR generating tags for Example {i} from {data_source_name} ---")
            print(f"Text: \"{text}\"")
            print(f"Entities (attempted sort): {sorted_entities if 'sorted_entities' in locals() else entities}")
            print(f"Error: {e}")
            misaligned_count +=1
            all_aligned = False
            continue
        if '-' in tags:
            misaligned_count += 1
            all_aligned = False
            print(f"\n--- MISALIGNMENT DETECTED IN EXAMPLE {i} from {data_source_name} ---")
            print(f"Text    : \"{text}\"")
            corrected_entities_for_print = []
            for start, end, label in entities:
                try: # Add try-except for robust text slicing
                    entity_text = text[start:end]
                    corrected_entities_for_print.append(f"('{entity_text}', {start}, {end}, '{label}')")
                except TypeError: # If start/end are not sliceable (e.g. None)
                    corrected_entities_for_print.append(f"(ERROR SLICING, {start}, {end}, '{label}')")

            print(f"Entities: {corrected_entities_for_print}")
            tokens_with_indices = []
            for t_idx, token in enumerate(doc):
                tokens_with_indices.append(f"('{token.text}', {token.idx}, {tags[t_idx]})")
            print(f"Tokens (text, char_idx, BILUO_tag): {tokens_with_indices}")
            for ent_idx, (start_char, end_char, label) in enumerate(entities):
                found_problem_for_entity = False
                for tok_idx, tag_char in enumerate(tags):
                    token = doc[tok_idx]
                    token_start = token.idx
                    token_end = token.idx + len(token.text)
                    overlap = (start_char < token_end) and (end_char > token_start)
                    if tag_char == '-' and overlap:
                        try:
                            ent_text_display = text[start_char:end_char]
                        except TypeError:
                            ent_text_display = "[ERROR DISPLAYING ENTITY TEXT]"
                        print(f"  Problem likely related to Entity #{ent_idx}: ('{ent_text_display}', {start_char}, {end_char}, '{label}')")
                        print(f"  This entity might be misaligned with Token: ('{token.text}', char_idx {token.idx}, BILUO tag '{tag_char}')")
                        found_problem_for_entity = True
                        break
                if found_problem_for_entity:
                    pass
            print("  Common issues:")
            print("  - Entity span includes leading/trailing space relative to a token.")
            print("  - Entity span starts or ends in the middle of a token.")
            print("  - Off-by-one error in span definition.")
            print("  - Entity spans whitespace that spaCy tokenizes separately.")
    if misaligned_count == 0:
        print(f"\n>>> All {data_source_name} examples are correctly aligned!")
    else:
        print(f"\n>>> Found {misaligned_count} {data_source_name} examples with misalignments. Please fix them for best results.")
    print(f"--- End of alignment check for {data_source_name} ---\n")
    return all_aligned


# --- train_ner_model (Keep your robust version) ---
def train_ner_model(train_data, model_output_dir, n_iter=N_ITERATIONS, dropout=DROPOUT_RATE, base_nlp=None):
    # ... (Your existing detailed train_ner_model function) ...
    # Ensure it correctly processes entities as tuples.
    if not train_data:
        print("Training data is empty. Skipping training.")
        return None
    if base_nlp is None:
        nlp = spacy.blank("en")
        print("Created blank 'en' model for training.")
    else:
        nlp = base_nlp
        print("Using provided 'en' model for training.")

    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    all_labels = set()
    for _, annotations in train_data:
        for ent_tuple in annotations.get("entities", []):
            if isinstance(ent_tuple, tuple) and len(ent_tuple) == 3:
                all_labels.add(ent_tuple[2])
            else:
                print(f"Warning: Malformed entity found: {ent_tuple} in annotations {annotations}")
    for label in sorted(list(all_labels)):
        ner.add_label(label)
    print(f"NER labels being trained: {sorted(list(all_labels))}")

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print("Starting training...")
        for iteration in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            batch_count = 0
            skipped_count = 0
            for text, annotations in train_data:
                try:
                    doc = nlp.make_doc(text)
                    current_entities = annotations.get("entities", [])
                    entities_as_tuples = [tuple(ent) for ent in current_entities if isinstance(ent, (list, tuple)) and len(ent) == 3]
                    sorted_entities_tuples = sorted(entities_as_tuples, key=lambda x: x[0])
                    example = Example.from_dict(doc, {"entities": sorted_entities_tuples})
                    nlp.update([example], sgd=optimizer, drop=dropout, losses=losses)
                    batch_count += 1
                except ValueError as e:
                    print(f"\nSkipping example during nlp.update (iter {iteration+1}): Text: \"{text[:100]}...\" Error: {e}")
                    skipped_count += 1
                    continue
            print(f"Iteration {iteration + 1}/{n_iter}, Losses: {losses}, Skipped: {skipped_count}")
            if skipped_count == len(train_data) and iteration > 1: # Stop if all are skipped after 2nd iteration
                print("ERROR: All training examples are being skipped consistently. Check data format/alignment.")
                return None # Indicate training failure

    if model_output_dir is not None:
        model_output_dir.mkdir(parents=True, exist_ok=True)
        nlp.to_disk(model_output_dir)
        print(f"Saved model to {model_output_dir}")
    return nlp


if __name__ == "__main__":
    # --- Load manually curated training data from JSON ---
    manual_train_data = load_train_data_from_json(TRAIN_DATA_JSON_PATH)

    # --- Load data from Label Studio (optional) ---
    label_studio_data = []
    if LABEL_STUDIO_JSON_PATH.exists():
        label_studio_data = convert_label_studio_to_training_data(LABEL_STUDIO_JSON_PATH)
    else:
        print(f"Label Studio export file not found at {LABEL_STUDIO_JSON_PATH}, skipping.")

    # --- Combine training data sources ---
    combined_train_data = []
    if manual_train_data:
        print(f"Using {len(manual_train_data)} examples from {TRAIN_DATA_JSON_PATH}.")
        combined_train_data.extend(manual_train_data)
    if label_studio_data:
        print(f"Adding {len(label_studio_data)} examples from Label Studio to the training set.")
        combined_train_data.extend(label_studio_data)

    seen_texts = set()
    unique_combined_train_data = []
    for item in combined_train_data:
        if not (isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[0], str)):
            print(f"Warning: Skipping malformed top-level item in combined_train_data: {item}")
            continue
        text = item[0]
        if text not in seen_texts:
            # Ensure entities within this item are tuples
            annots = item[1]
            if isinstance(annots, dict) and "entities" in annots:
                annots["entities"] = [tuple(e) for e in annots["entities"] if isinstance(e, (list,tuple)) and len(e)==3]
            unique_combined_train_data.append((text, annots))
            seen_texts.add(text)
    combined_train_data = unique_combined_train_data
    print(f"Total unique training examples after combining and deduplicating: {len(combined_train_data)}.")

    if not combined_train_data:
        print("No training data available. Exiting.")
        sys.exit(1)

    nlp_for_check_and_train = spacy.blank("en")

    data_is_aligned = check_data_alignment(combined_train_data, nlp_for_check_and_train, data_source_name="COMBINED_TRAIN_DATA")

    if not data_is_aligned:
        print("WARNING: Misalignments detected. Training may be suboptimal or fail.")
        user_choice = input("Proceed with training despite alignment warnings? (yes/no): ").lower()
        if user_choice != 'yes':
            sys.exit("Exiting: Data alignment issues need fixing.")
        print("Proceeding with training despite alignment warnings...\n")
    else:
        print("Data alignment check passed. Proceeding with training...\n")

    print(f"Starting training with {len(combined_train_data)} examples...")
    trained_nlp = train_ner_model(combined_train_data, MODEL_OUTPUT_DIR, base_nlp=nlp_for_check_and_train)

    if trained_nlp:
        print("Training complete.")
        if MODEL_OUTPUT_DIR:
            print(f"To use the model, load it from: {MODEL_OUTPUT_DIR}")
    else:
        print("Training did not complete successfully.")
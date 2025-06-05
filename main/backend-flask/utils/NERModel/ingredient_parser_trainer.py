import json
import sys
import spacy
import random
from spacy.training.example import Example
from spacy.training.iob_utils import offsets_to_biluo_tags
from pathlib import Path
from sklearn.model_selection import train_test_split
# from spacy.scorer import Scorer # Scorer is not directly used, evaluate uses nlp.evaluate

# --- NEW: Import TRAIN_DATA from save_data module (MOVED TO TOP FOR ROBUSTNESS) ---
try:
    # Assuming save_data.py is in the same directory or accessible via PYTHONPATH
    from save_data import TRAIN_DATA as MODULE_TRAIN_DATA
    print("Successfully imported TRAIN_DATA from save_data.py")
except ImportError:
    print("Error: Could not import TRAIN_DATA from save_data.py.")
    print("Please ensure save_data.py exists in the same directory and defines a variable named TRAIN_DATA.")
    sys.exit(1)


# --- GPU Configuration ---
try:
    spacy.require_gpu()
    print("Successfully enabled GPU.")
except Exception as e:
    print(f"GPU not available or could not be enabled: {e}. Falling back to CPU.")

# --- Model training configuration ---
TRAIN_DATA_JSON_PATH = Path("./train_data.json") # This path is now technically ignored by the modified function
LABEL_STUDIO_JSON_PATH = Path("./label_studio_export.json")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_OUTPUT_DIR_BASE = PROJECT_ROOT / "models" / "ingredient_ner_model_patience_stop" # New dir
MAX_TOTAL_ITERATIONS = 400  # Maximum possible iterations (safety cap)
DROPOUT_RATE = 0.4
DEV_SPLIT_SIZE = 0.20
EVAL_FREQUENCY = 1          # Evaluate on dev set every N iterations

# --- NEW Early Stopping Configuration ---
PATIENCE_NO_NEW_BEST_SCORE = 40 # Number of evaluation periods without a new best score
# If EVAL_FREQUENCY is 1, this means 30 training iterations without improvement.

# --- NEW: Training Batch Size for nlp.update() ---
TRAINING_BATCH_SIZE = 32 # This is crucial for speed. Adjust based on your GPU/CPU memory and data.

# --- Helper functions ---

# --- MODIFIED FUNCTION WITH VERBOSE LOGGING ---
def load_train_data_from_json(json_path):
    """
    Loads training data.
    IMPORTANT: This function is now modified to directly return the 'TRAIN_DATA'
    variable imported from 'save_data.py', rather than reading from a JSON file.
    The 'json_path' parameter is kept for signature compatibility but is ignored.
    Includes verbose logging to help debug data format issues.
    """
    print(f"INFO: 'load_train_data_from_json' is now loading data from 'save_data.py :: TRAIN_DATA'. The provided json_path '{json_path}' is ignored.")
    processed_train_data = []

    # Check if MODULE_TRAIN_DATA is actually populated and iterable
    if not isinstance(MODULE_TRAIN_DATA, list) or not MODULE_TRAIN_DATA:
        print(f"ERROR: MODULE_TRAIN_DATA from save_data.py is empty or not a list. Current type: {type(MODULE_TRAIN_DATA)}")
        return []

    for idx, item in enumerate(MODULE_TRAIN_DATA):
        if isinstance(item, (list, tuple)) and len(item) == 2:
            text, annotations_dict = item
            if not isinstance(text, str):
                print(f"Warning (Item {idx}): Text is not a string. Skipping item: {item}")
                continue

            if isinstance(annotations_dict, dict) and "entities" in annotations_dict:
                entities_as_tuples = []
                all_original_entities_valid = True
                for ent_idx_orig, ent_orig in enumerate(annotations_dict["entities"]):
                    if isinstance(ent_orig, (list, tuple)) and len(ent_orig) == 3:
                        start, end, label = ent_orig
                        if isinstance(start, int) and isinstance(end, int) and isinstance(label, str):
                            entities_as_tuples.append(tuple(ent_orig))
                        else:
                            print(f"Warning (Item {idx}, Entity {ent_idx_orig}): Malformed entity component types. Expected (int, int, str), got ({type(start)}, {type(end)}, {type(label)}). Entity: {ent_orig}. Text preview: '{text[:50]}...'")
                            all_original_entities_valid = False
                            break # Skip this item entirely if any entity is malformed
                    else:
                        print(f"Warning (Item {idx}, Entity {ent_idx_orig}): Malformed entity structure. Expected list/tuple of length 3, got {type(ent_orig)} of length {len(ent_orig) if isinstance(ent_orig, (list,tuple)) else 'N/A'}. Entity: {ent_orig}. Text preview: '{text[:50]}...'")
                        all_original_entities_valid = False
                        break # Skip this item entirely if any entity is malformed

                if all_original_entities_valid:
                    # Check if the number of successfully processed entities matches the original count
                    if len(entities_as_tuples) == len(annotations_dict["entities"]):
                        processed_train_data.append((text, {"entities": entities_as_tuples}))
                    else:
                        print(f"Warning (Item {idx}): Mismatch in entity count after validation. Original: {len(annotations_dict['entities'])}, Validated: {len(entities_as_tuples)}. Skipping item. Text preview: '{text[:50]}...'")
                else:
                    print(f"Warning (Item {idx}): Skipping item due to internal malformed entities. Text preview: '{text[:50]}...'")
            else:
                print(f"Warning (Item {idx}): Malformed annotation structure. Expected dict with 'entities' key, got {type(annotations_dict)}. Item: {item}. Text preview: '{text[:50]}...'")
        else:
            print(f"Warning (Item {idx}): Malformed top-level item. Expected list/tuple of 2 elements, got {type(item)} of length {len(item) if isinstance(item, (list,tuple)) else 'N/A'}. Item: {item}")
    print(f"Successfully loaded and processed {len(processed_train_data)} examples from MODULE_TRAIN_DATA.")
    return processed_train_data

def convert_label_studio_to_training_data(label_studio_json_path):
    """Converts Label Studio JSON export to a common NER training data format."""
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
    for item in data_items:
        text = item.get('data', {}).get('text')
        if not text: continue
        annotations_list = item.get('annotations', [])
        if annotations_list and isinstance(annotations_list, list) and len(annotations_list) > 0:
            annotation_set = annotations_list[0]
            if 'result' in annotation_set and isinstance(annotation_set['result'], list):
                annotation_results = annotation_set['result']
                entities = []
                for result in annotation_results:
                    if (result.get('type') == 'labels' and 'value' in result and isinstance(result['value'], dict)):
                        val = result['value']
                        if ('start' in val and isinstance(val['start'], int) and
                                'end' in val and isinstance(val['end'], int) and
                                val.get('labels') and isinstance(val['labels'], list) and val['labels']):
                            if 0 <= val['start'] <= val['end'] <= len(text):
                                entities.append( (val['start'], val['end'], val['labels'][0]) )
                            # else: # Commented out for less verbose output
                            #     print(f"Warning: Invalid offsets in Label Studio data for text '{text[:50]}...': start={val['start']}, end={val['end']}, len={len(text)}")
                if entities:
                    converted_data.append((text, {"entities": entities}))
    print(f"Successfully converted {len(converted_data)} items from Label Studio export.")
    return converted_data

def check_data_alignment(data_to_check, nlp_tokenizer, data_source_name="TRAIN_DATA"):
    """
    Checks for alignment issues in training data.
    Takes an nlp_tokenizer (a blank spaCy model with just a tokenizer) for speed.
    """
    print(f"\n--- Checking {data_source_name} for alignment issues ---")
    misaligned_count = 0
    all_aligned = True
    for i, (text, annotation) in enumerate(data_to_check):
        # Use the provided nlp_tokenizer for faster doc creation
        doc = nlp_tokenizer.make_doc(text)
        entities = annotation.get("entities", [])
        if not entities:
            continue

        try:
            current_entities_as_tuples = []
            for ent_idx_orig, ent_orig in enumerate(entities):
                if isinstance(ent_orig, (list, tuple)) and len(ent_orig) == 3:
                    if isinstance(ent_orig[0], int) and isinstance(ent_orig[1], int) and isinstance(ent_orig[2], str):
                        current_entities_as_tuples.append(tuple(ent_orig))
                # else: # Commented out for less verbose output
                #     print(f"Warning: Malformed entity content in example {i} (original index {ent_idx_orig}), text '{text[:50]}...'. Entity: {ent_orig}")

            if entities and not current_entities_as_tuples and len(entities) != len(current_entities_as_tuples):
                misaligned_count += 1
                all_aligned = False
                continue

            sorted_entities = sorted(current_entities_as_tuples, key=lambda x: x[0])
            tags = offsets_to_biluo_tags(doc, sorted_entities)

        except ValueError as e:
            print(f"\n--- ERROR generating tags for Example {i} from {data_source_name} ---")
            print(f"Text: \"{text}\"")
            entities_to_print_on_error = locals().get('sorted_entities', entities)
            print(f"Entities (attempted sort): {entities_to_print_on_error}")
            print(f"Error: {e}")
            misaligned_count +=1
            all_aligned = False
            continue
        except Exception as e:
            print(f"\n--- UNEXPECTED ERROR generating tags for Example {i} from {data_source_name} ---")
            print(f"Text: \"{text}\"")
            entities_to_print_on_error = locals().get('sorted_entities', entities)
            print(f"Entities (attempted sort): {entities_to_print_on_error}")
            print(f"Error: {e}")
            misaligned_count +=1
            all_aligned = False
            continue

        if '-' in tags:
            misaligned_count += 1
            all_aligned = False
            print(f"\n--- MISALIGNMENT DETECTED IN EXAMPLE {i} from {data_source_name} ---")
            print(f"Text    : \"{text}\"")

            entities_for_print_str = []
            for ent_s, ent_e, ent_l in sorted_entities:
                try:
                    ent_text_display = text[ent_s:ent_e]
                    entities_for_print_str.append(f"('{ent_text_display}', {ent_s}, {ent_e}, '{ent_l}')")
                except TypeError:
                    entities_for_print_str.append(f"(ERROR_SLICING: s={ent_s}, e={ent_e}, l='{ent_l}')")
                except IndexError:
                    entities_for_print_str.append(f"(INDEX_ERROR: s={ent_s}, e={ent_e}, l='{ent_l}')")
            print(f"Entities: {entities_for_print_str}")

            tokens_with_biluo = [(token.text, token.idx, tags[j]) for j, token in enumerate(doc)]
            print(f"Tokens (text, char_idx, BILUO_tag): {tokens_with_biluo}")

            identified_problem_entity_in_log = False
            for ent_idx_sorted, (start_char, end_char, label) in enumerate(sorted_entities):
                problem_token_for_current_entity = None
                for tok_idx, token in enumerate(doc):
                    token_start = token.idx
                    token_end = token.idx + len(token.text)
                    if max(start_char, token_start) < min(end_char, token_end):
                        if tags[tok_idx] == '-':
                            problem_token_for_current_entity = token
                            break
                if problem_token_for_current_entity:
                    try:
                        ent_text_display = text[start_char:end_char]
                    except:
                        ent_text_display = "[ERROR DISPLAYING ENTITY TEXT]"
                    print(f"  Problem likely related to Entity #{ent_idx_sorted} (in sorted list): ('{ent_text_display}', {start_char}, {end_char}, '{label}')")
                    print(f"  This entity might be misaligned with Token: ('{problem_token_for_current_entity.text}', char_idx {problem_token_for_current_entity.idx}, BILUO tag '-')")
                    identified_problem_entity_in_log = True
                    break

            if not identified_problem_entity_in_log:
                print("  A misaligned token ('-') exists, but the exact problematic entity/token pair was not pinpointed by the simple overlap check. Review all entities and their token alignments carefully.")
            print("  Common issues:")
            print("  - Entity span includes leading/trailing space relative to a token.")
            print("  - Entity span starts or ends in the middle of a token.")
            print("  - Off-by-one error in span definition.")
            print("  - Entity spans whitespace that spaCy tokenizes separately.")
            print("  - Overlapping entities (check for [E103] errors higher up if any).")

    if misaligned_count == 0:
        print(f"\n>>> All {data_source_name} examples are correctly aligned!")
    else:
        print(f"\n>>> Found {misaligned_count} {data_source_name} examples with misalignments. Please fix them.")
    print(f"--- End of alignment check for {data_source_name} ---\n")
    return all_aligned

def evaluate(nlp, examples):
    """Evaluate the model on a list of examples."""
    eval_examples = []
    for text, annotations in examples:
        doc_for_example = nlp.make_doc(text)
        entities_as_tuples = [tuple(ent) for ent in annotations.get("entities", []) if isinstance(ent, (list, tuple)) and len(ent) == 3]
        sorted_entities_tuples = sorted(entities_as_tuples, key=lambda x: x[0])
        eval_examples.append(Example.from_dict(doc_for_example, {"entities": sorted_entities_tuples}))
    if not eval_examples:
        return {"ents_f": 0.0, "ents_p": 0.0, "ents_r": 0.0, "ents_per_type": {}}
    scores = nlp.evaluate(eval_examples)
    return scores


def train_ner_model(train_data, dev_data, model_output_dir_base,
                    max_iter=MAX_TOTAL_ITERATIONS, dropout=DROPOUT_RATE, base_nlp=None):

    if not train_data:
        print("Training data is empty. Skipping training.")
        return None

    # Use a blank English model if no base_nlp provided, it's faster for pure NER from scratch.
    if base_nlp is None:
        nlp = spacy.blank("en")
        print("Created blank 'en' model for training.")
    else:
        nlp = base_nlp
        print("Using provided model for training.")

    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    all_labels = set()
    for _, annotations in train_data + (dev_data if dev_data else []):
        for ent_tuple in annotations.get("entities", []):
            if isinstance(ent_tuple, tuple) and len(ent_tuple) == 3:
                all_labels.add(ent_tuple[2])
    all_labels.discard('O') # 'O' is not a real label, it's a tag for non-entities.
    for label in sorted(list(all_labels)):
        ner.add_label(label)
    print(f"NER labels being trained: {sorted(list(all_labels))}")

    best_dev_f_score = -1.0
    best_model_path = None
    evaluations_since_new_best = 0

    current_iteration = 0
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    with nlp.disable_pipes(*other_pipes): # Disable other pipes during training for NER
        optimizer = nlp.begin_training()
        print(f"Starting training with batch size: {TRAINING_BATCH_SIZE}")
        while current_iteration < max_iter:
            current_iteration += 1
            random.shuffle(train_data)
            losses = {}
            skipped_count = 0
            batch = [] # Accumulate examples for batch update

            for text, annotations in train_data:
                try:
                    doc = nlp.make_doc(text)
                    current_entities = annotations.get("entities", [])
                    entities_as_tuples = [tuple(ent) for ent in current_entities if isinstance(ent, (list, tuple)) and len(ent) == 3]
                    sorted_entities_tuples = sorted(entities_as_tuples, key=lambda x: x[0])
                    example = Example.from_dict(doc, {"entities": sorted_entities_tuples})
                    batch.append(example)

                    if len(batch) >= TRAINING_BATCH_SIZE:
                        nlp.update(batch, sgd=optimizer, drop=dropout, losses=losses)
                        batch.clear() # Clear the batch after updating
                except ValueError as e:
                    # print(f"Skipping example during nlp.update (iter {current_iteration}): Text: \"{text[:70]}...\" Error: {e}") # Commented out for less verbose output
                    skipped_count += 1
                except Exception as e: # Catch any other unexpected errors during example processing
                    # print(f"Skipping example due to unexpected error (iter {current_iteration}): Text: \"{text[:70]}...\" Error: {e}") # Commented out
                    skipped_count += 1

            # Process any remaining examples in the batch after the loop
            if batch:
                nlp.update(batch, sgd=optimizer, drop=dropout, losses=losses)
                batch.clear()

            print(f"Iter {current_iteration}/{max_iter}, Losses: {losses.get('ner', 0.0):.4f}, Skipped: {skipped_count}")

            if skipped_count == len(train_data) and current_iteration > 1 :
                print("ERROR: All training examples are being skipped consistently. Check data format/alignment.")
                return None

            # --- Evaluation and Early Stopping Logic ---
            if dev_data and (current_iteration % EVAL_FREQUENCY == 0):
                # print(f"\n--- Evaluating on Dev Set (End of Iter {current_iteration}) ---") # Commented out for less verbose output
                dev_scores = evaluate(nlp, dev_data)
                current_f_score = dev_scores.get("ents_f", 0.0)
                print(f"Dev Scores (Iter {current_iteration}): P: {dev_scores.get('ents_p', 0.0):.4f}, R: {dev_scores.get('ents_r', 0.0):.4f}, F: {current_f_score:.4f}")

                if current_f_score > best_dev_f_score:
                    best_dev_f_score = current_f_score
                    evaluations_since_new_best = 0
                    if model_output_dir_base:
                        # Use a more generic best model path, not tied to iteration
                        # You could save per-iteration best models if disk space allows and you want to debug progression
                        current_best_path = model_output_dir_base / "model_best"
                        current_best_path.mkdir(parents=True, exist_ok=True)
                        nlp.to_disk(current_best_path)
                        best_model_path = current_best_path
                        print(f"New best model saved to {best_model_path} with F-score: {best_dev_f_score:.4f}")
                else:
                    evaluations_since_new_best += 1
                    print(f"Dev F-score ({current_f_score:.4f}) did not exceed best ({best_dev_f_score:.4f}). Evals since new best: {evaluations_since_new_best}.") # Commented out for less verbose output

                if evaluations_since_new_best >= PATIENCE_NO_NEW_BEST_SCORE:
                    print(f"\nEarly stopping: Dev F-score has not achieved a new best for {PATIENCE_NO_NEW_BEST_SCORE} consecutive evaluation periods.")
                    break
    # End of while loop

    if current_iteration >= max_iter:
        print(f"\nReached maximum configured iterations ({max_iter}).")

    # Save final model from the last iteration (might not be the best but is the latest state)
    if model_output_dir_base:
        final_model_path = model_output_dir_base / "model_final"
        final_model_path.mkdir(parents=True, exist_ok=True)
        nlp.to_disk(final_model_path)
        print(f"Saved final model (from iter {current_iteration}) to {final_model_path}")

    if best_model_path:
        print(f"\nBest performing model on dev set was saved to: {best_model_path} (F-score: {best_dev_f_score:.4f})")
    elif dev_data:
        print("\nNo best model saved (e.g., dev F-score never improved or dev set was empty).")

    return nlp

if __name__ == "__main__":
    manual_train_data = load_train_data_from_json(TRAIN_DATA_JSON_PATH)
    label_studio_data = convert_label_studio_to_training_data(LABEL_STUDIO_JSON_PATH)

    combined_data_raw = []
    if manual_train_data: combined_data_raw.extend(manual_train_data)
    if label_studio_data: combined_data_raw.extend(label_studio_data)

    seen_texts = set()
    unique_combined_data = []
    for item in combined_data_raw:
        if not (isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[0], str)):
            # print(f"Warning: Skipping malformed top-level item: {item}") # This was previously commented, keeping it that way, but load_train_data_from_json will catch issues anyway now.
            continue
        text, annots = item
        if text not in seen_texts:
            if isinstance(annots, dict) and "entities" in annots:
                annots["entities"] = [tuple(e) for e in annots["entities"] if isinstance(e, (list,tuple)) and len(e)==3]
            unique_combined_data.append((text, annots))
            seen_texts.add(text)

    print(f"Total unique examples: {len(unique_combined_data)}.")

    if not unique_combined_data:
        print("No training data. Exiting.")
        sys.exit(1)

    train_examples, dev_examples = [], []
    if DEV_SPLIT_SIZE > 0 and len(unique_combined_data) >= (1 / DEV_SPLIT_SIZE if DEV_SPLIT_SIZE > 0 else float('inf')):
        train_examples, dev_examples = train_test_split(
            unique_combined_data, test_size=DEV_SPLIT_SIZE, random_state=42, shuffle=True
        )
    else:
        train_examples = unique_combined_data
        if DEV_SPLIT_SIZE > 0 :
            print(f"Warning: Dataset too small ({len(unique_combined_data)}) for a {DEV_SPLIT_SIZE*100}% dev split. Training on all data.")
        else:
            print("DEV_SPLIT_SIZE is 0. Training on all data. No dev evaluation during training for early stopping.")
        dev_examples = []

    print(f"Training examples: {len(train_examples)}, Development examples: {len(dev_examples)}")

    # Use spacy.blank("en") for alignment check as it's much faster than en_core_web_md
    nlp_for_alignment_check = spacy.blank("en")
    train_aligned = check_data_alignment(train_examples, nlp_for_alignment_check, "TRAIN_DATA")
    dev_aligned = True
    if dev_examples:
        dev_aligned = check_data_alignment(dev_examples, nlp_for_alignment_check, "DEV_DATA")

    if not (train_aligned and dev_aligned):
        print("WARNING: Misalignments detected. Training may be suboptimal.")
        if input("Proceed? (yes/no): ").lower() != 'yes':
            sys.exit("Exiting: Fix alignment issues.")
        print("Proceeding despite warnings...\n")
    else:
        print("Alignment checks passed. Proceeding...\n")

    # Start training from a blank 'en' model for speed if you don't need pre-trained vectors.
    # If you need pre-trained vectors (e.g., if you have very little data),
    # change spacy.blank("en") to spacy.load("en_core_web_md", disable=["parser", "tagger", "attribute_ruler", "lemmatizer", "textcat", "senter"])
    # nlp_to_train = spacy.blank("en")
    nlp_to_train = spacy.load("en_core_web_md", disable=["parser", "tagger", "attribute_ruler", "lemmatizer", "textcat", "senter"]) # Alternative if you want vectors

    print(f"Starting training (max {MAX_TOTAL_ITERATIONS} iters), evaluating every {EVAL_FREQUENCY} iters.")
    print(f"Early stopping patience: training will stop if no new best dev F-score is found after {PATIENCE_NO_NEW_BEST_SCORE} evaluation periods (i.e., {PATIENCE_NO_NEW_BEST_SCORE * EVAL_FREQUENCY} training iterations without improvement).")

    trained_nlp = train_ner_model(
        train_examples,
        dev_examples,
        MODEL_OUTPUT_DIR_BASE,
        max_iter=MAX_TOTAL_ITERATIONS,
        dropout=DROPOUT_RATE,
        base_nlp=nlp_to_train # Pass the pre-loaded/pre-blanked NLP object
    )

    if trained_nlp: print("\n--- Training process finished. ---")
    else: print("\n--- Training did not complete successfully. ---")
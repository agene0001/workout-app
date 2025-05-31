import json
import sys
import spacy
import random
from spacy.training.example import Example
from spacy.training.iob_utils import offsets_to_biluo_tags
from pathlib import Path
from sklearn.model_selection import train_test_split
from spacy.scorer import Scorer

# --- GPU Configuration (same as before) ---
try:
    spacy.require_gpu()
    print("Successfully enabled GPU.")
except Exception as e:
    print(f"GPU not available or could not be enabled: {e}. Falling back to CPU.")

# --- Model training configuration ---
TRAIN_DATA_JSON_PATH = Path("./train_data.json")
LABEL_STUDIO_JSON_PATH = Path("./label_studio_export.json")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MODEL_OUTPUT_DIR_BASE = PROJECT_ROOT / "models" / "ingredient_ner_model_patience_stop" # New dir
MAX_TOTAL_ITERATIONS = 400  # Maximum possible iterations (safety cap)
DROPOUT_RATE = 0.35
DEV_SPLIT_SIZE = 0.20
EVAL_FREQUENCY = 1          # Evaluate on dev set every 5 iterations

# --- NEW Early Stopping Configuration ---
# Stop if dev F-score has not achieved a NEW BEST score for this many consecutive evaluation periods.
# This is your "buffer of 5-10 epochs" (if EVAL_FREQUENCY=1) or evaluation cycles.
# Example: If EVAL_FREQUENCY is 5, and PATIENCE_NO_NEW_BEST_SCORE is 3,
# this means (3 * 5 = 15) training iterations without achieving a new best F-score.
PATIENCE_NO_NEW_BEST_SCORE = 20 # Adjust this: e.g., 2 means 2*EVAL_FREQUENCY iterations without new best.
# If you want 5-10 actual *training epochs* (iterations in spaCy terms)
# and EVAL_FREQUENCY is 5, then set this to 1 or 2.
# If EVAL_FREQUENCY is 1, then set this to 5-10.

# --- load_train_data_from_json, convert_label_studio_to_training_data, check_data_alignment, evaluate functions (SAME AS PREVIOUS GOOD ANSWER) ---
# Make sure these functions are copied from the previous complete answer.
# For brevity, I'm omitting them here, but they are essential.
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
                        entities_as_tuples = [tuple(ent) for ent in annotations_dict["entities"] if isinstance(ent, list) and len(ent) == 3]
                        if len(entities_as_tuples) == len(annotations_dict["entities"]):
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
                            else:
                                print(f"Warning: Invalid offsets in Label Studio data for text '{text[:50]}...': start={val['start']}, end={val['end']}, len={len(text)}")
                if entities:
                    converted_data.append((text, {"entities": entities}))
    print(f"Successfully converted {len(converted_data)} items from Label Studio export.")
    return converted_data

def check_data_alignment(data_to_check, nlp_model, data_source_name="TRAIN_DATA"):
    print(f"\n--- Checking {data_source_name} for alignment issues ---")
    misaligned_count = 0
    all_aligned = True
    for i, (text, annotation) in enumerate(data_to_check):
        doc = nlp_model.make_doc(text)
        entities = annotation.get("entities", [])
        if not entities:
            continue

        # Ensure entities are tuples and sorted by start offset
        try:
            current_entities_as_tuples = []
            for ent_idx_orig, ent_orig in enumerate(entities):
                if isinstance(ent_orig, (list, tuple)) and len(ent_orig) == 3:
                    # Basic type check for start, end, label
                    if isinstance(ent_orig[0], int) and isinstance(ent_orig[1], int) and isinstance(ent_orig[2], str):
                        current_entities_as_tuples.append(tuple(ent_orig))
                    else:
                        print(f"Warning: Malformed entity content in example {i} (original index {ent_idx_orig}), text '{text[:50]}...'. Entity: {ent_orig}")
                else:
                    print(f"Warning: Malformed entity structure in example {i} (original index {ent_idx_orig}), text '{text[:50]}...'. Entity: {ent_orig}")

            # If malformed entities were found and skipped, and this results in an empty list for a non-empty original
            if entities and not current_entities_as_tuples and len(entities) != len(current_entities_as_tuples):
                print(f"Skipping alignment check for example {i} due to all entities being malformed.")
                misaligned_count += 1
                all_aligned = False
                continue

            # Sort entities by start offset to prevent spaCy errors with unsorted entities
            # This also helps in identifying the first problematic entity more easily
            sorted_entities = sorted(current_entities_as_tuples, key=lambda x: x[0])

            tags = offsets_to_biluo_tags(doc, sorted_entities)

        except ValueError as e: # Catches errors from offsets_to_biluo_tags (e.g., overlapping entities [E103])
            print(f"\n--- ERROR generating tags for Example {i} from {data_source_name} ---")
            print(f"Text: \"{text}\"")
            # Use sorted_entities if available from the try block, otherwise original entities list
            entities_to_print_on_error = locals().get('sorted_entities', entities)
            print(f"Entities (attempted sort): {entities_to_print_on_error}")
            print(f"Error: {e}")
            misaligned_count +=1
            all_aligned = False
            continue
        except Exception as e: # Catch any other unexpected errors during tag generation
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
            for ent_s, ent_e, ent_l in sorted_entities: # Use sorted_entities for consistency with tags
                try:
                    ent_text_display = text[ent_s:ent_e]
                    entities_for_print_str.append(f"('{ent_text_display}', {ent_s}, {ent_e}, '{ent_l}')")
                except TypeError: # Handle if s or e are not int
                    entities_for_print_str.append(f"(ERROR_SLICING: s={ent_s}, e={ent_e}, l='{ent_l}')")
                except IndexError: # Handle if s or e are out of bounds for text
                    entities_for_print_str.append(f"(INDEX_ERROR: s={ent_s}, e={ent_e}, l='{ent_l}')")

            print(f"Entities: {entities_for_print_str}")

            tokens_with_biluo = [(token.text, token.idx, tags[j]) for j, token in enumerate(doc)]
            print(f"Tokens (text, char_idx, BILUO_tag): {tokens_with_biluo}")

            # --- Logic to pinpoint problematic entity ---
            identified_problem_entity_in_log = False
            for ent_idx_sorted, (start_char, end_char, label) in enumerate(sorted_entities):
                # Iterate through tokens that this entity *should* cover
                problem_token_for_current_entity = None
                for tok_idx, token in enumerate(doc):
                    token_start = token.idx
                    token_end = token.idx + len(token.text)
                    # Check if the current token falls (at least partially) within the current entity's span
                    if max(start_char, token_start) < min(end_char, token_end): # Checks for overlap
                        if tags[tok_idx] == '-':
                            problem_token_for_current_entity = token
                            break # Found a misaligned token for this entity

                if problem_token_for_current_entity:
                    try:
                        ent_text_display = text[start_char:end_char]
                    except:
                        ent_text_display = "[ERROR DISPLAYING ENTITY TEXT]"
                    print(f"  Problem likely related to Entity #{ent_idx_sorted} (in sorted list): ('{ent_text_display}', {start_char}, {end_char}, '{label}')")
                    print(f"  This entity might be misaligned with Token: ('{problem_token_for_current_entity.text}', char_idx {problem_token_for_current_entity.idx}, BILUO tag '-')")
                    identified_problem_entity_in_log = True
                    break # Show the first problematic entity and its problematic token for this example

            if not identified_problem_entity_in_log: # Fallback if specific token not pinpointed but '-' exists
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

    if base_nlp is None:
        nlp = spacy.blank("en_core_web_md")
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
    all_labels.discard('O')
    for label in sorted(list(all_labels)):
        ner.add_label(label)
    print(f"NER labels being trained: {sorted(list(all_labels))}")

    best_dev_f_score = -1.0  # Initialize best score to a very low value
    best_model_path = None

    # Early stopping counter: number of evaluations since a new best F-score was achieved
    evaluations_since_new_best = 0

    current_iteration = 0
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print("Starting training...")
        while current_iteration < max_iter:
            current_iteration += 1
            random.shuffle(train_data)
            losses = {}
            skipped_count = 0
            for text, annotations in train_data:
                try:
                    doc = nlp.make_doc(text)
                    current_entities = annotations.get("entities", [])
                    entities_as_tuples = [tuple(ent) for ent in current_entities if isinstance(ent, (list, tuple)) and len(ent) == 3]
                    sorted_entities_tuples = sorted(entities_as_tuples, key=lambda x: x[0])
                    example = Example.from_dict(doc, {"entities": sorted_entities_tuples})
                    nlp.update([example], sgd=optimizer, drop=dropout, losses=losses)
                except ValueError as e:
                    print(f"Skipping example during nlp.update (iter {current_iteration}): Text: \"{text[:70]}...\" Error: {e}")
                    skipped_count += 1
            print(f"Iter {current_iteration}/{max_iter}, Losses: {losses.get('ner', 0.0):.4f}, Skipped: {skipped_count}")

            if skipped_count == len(train_data) and current_iteration > 1 :
                print("ERROR: All training examples are being skipped consistently. Check data format/alignment.")
                return None

            # --- Evaluation and Early Stopping Logic ---
            if dev_data and (current_iteration % EVAL_FREQUENCY == 0):
                print(f"\n--- Evaluating on Dev Set (End of Iter {current_iteration}) ---")
                dev_scores = evaluate(nlp, dev_data)
                current_f_score = dev_scores.get("ents_f", 0.0) # Default to 0.0 if 'ents_f' not found
                print(f"Dev Scores: P: {dev_scores.get('ents_p', 0.0):.4f}, R: {dev_scores.get('ents_r', 0.0):.4f}, F: {current_f_score:.4f}")
                # ents_per_type = dev_scores.get('ents_per_type', {})
                # if ents_per_type:
                #     for label, scores_dict in ents_per_type.items():
                #         print(f"  {label}: P: {scores_dict.get('p',0.0):.3f}, R: {scores_dict.get('r',0.0):.3f}, F: {scores_dict.get('f',0.0):.3f}")

                # Check if the current F-score is a new best
                if current_f_score > best_dev_f_score:
                    best_dev_f_score = current_f_score
                    evaluations_since_new_best = 0 # Reset counter because we found a new best
                    if model_output_dir_base:
                        current_best_path = model_output_dir_base / f"model_best_iter{current_iteration}"
                        current_best_path.mkdir(parents=True, exist_ok=True)
                        nlp.to_disk(current_best_path)
                        best_model_path = current_best_path
                        print(f"New best model saved to {best_model_path} with F-score: {best_dev_f_score:.4f}")
                else:
                    evaluations_since_new_best += 1
                    print(f"Dev F-score ({current_f_score:.4f}) did not exceed best ({best_dev_f_score:.4f}). Evals since new best: {evaluations_since_new_best}.")

                # Apply stopping condition
                if evaluations_since_new_best >= PATIENCE_NO_NEW_BEST_SCORE:
                    print(f"\nEarly stopping: Dev F-score has not achieved a new best for {PATIENCE_NO_NEW_BEST_SCORE} consecutive evaluation periods.")
                    break
                    # End of evaluation block
    # End of while loop (training iterations)

    if current_iteration >= max_iter:
        print(f"\nReached maximum configured iterations ({max_iter}).")

    # Save final model from the last iteration
    if model_output_dir_base:
        final_model_path = model_output_dir_base / "model_final"
        final_model_path.mkdir(parents=True, exist_ok=True)
        nlp.to_disk(final_model_path)
        print(f"Saved final model (from iter {current_iteration}) to {final_model_path}")

    if best_model_path:
        print(f"\nBest performing model on dev set was saved to: {best_model_path} (F-score: {best_dev_f_score:.4f})")
    elif dev_data: # Only print this message if we actually had a dev set to evaluate
        print("\nNo best model saved (e.g., dev F-score never improved enough to be saved or dev set was empty/not evaluated).")

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
            print(f"Warning: Skipping malformed top-level item: {item}")
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
    # Ensure there's enough data to split and DEV_SPLIT_SIZE is positive
    if DEV_SPLIT_SIZE > 0 and len(unique_combined_data) >= (1 / DEV_SPLIT_SIZE if DEV_SPLIT_SIZE > 0 else float('inf')): # e.g. at least 5 for 0.2 split
        train_examples, dev_examples = train_test_split(
            unique_combined_data, test_size=DEV_SPLIT_SIZE, random_state=42, shuffle=True
        )
    else:
        train_examples = unique_combined_data
        if DEV_SPLIT_SIZE > 0 :
            print(f"Warning: Dataset too small ({len(unique_combined_data)}) for a {DEV_SPLIT_SIZE*100}% dev split. Training on all data.")
        else:
            print("DEV_SPLIT_SIZE is 0. Training on all data. No dev evaluation during training for early stopping.")
        dev_examples = [] # Ensure dev_examples is an empty list if not split

    print(f"Training examples: {len(train_examples)}, Development examples: {len(dev_examples)}")

    nlp_for_alignment_check = spacy.load("en_core_web_md")
    train_aligned = check_data_alignment(train_examples, nlp_for_alignment_check, "TRAIN_DATA")
    dev_aligned = True # Default to true if no dev set
    if dev_examples: # Only check dev_examples if it's not empty
        dev_aligned = check_data_alignment(dev_examples, nlp_for_alignment_check, "DEV_DATA")

    if not (train_aligned and dev_aligned):
        print("WARNING: Misalignments detected. Training may be suboptimal.")
        if input("Proceed? (yes/no): ").lower() != 'yes':
            sys.exit("Exiting: Fix alignment issues.")
        print("Proceeding despite warnings...\n")
    else:
        print("Alignment checks passed. Proceeding...\n")

    nlp_to_train = spacy.load("en_core_web_md")

    # Ensure EVAL_FREQUENCY makes sense with PATIENCE_NO_NEW_BEST_SCORE
    print(f"Starting training (max {MAX_TOTAL_ITERATIONS} iters), evaluating every {EVAL_FREQUENCY} iters.")
    print(f"Early stopping patience: training will stop if no new best dev F-score is found after {PATIENCE_NO_NEW_BEST_SCORE} evaluation periods (i.e., {PATIENCE_NO_NEW_BEST_SCORE * EVAL_FREQUENCY} training iterations without improvement).")

    trained_nlp = train_ner_model(
        train_examples,
        dev_examples,
        MODEL_OUTPUT_DIR_BASE,
        max_iter=MAX_TOTAL_ITERATIONS,
        dropout=DROPOUT_RATE,
        base_nlp=nlp_to_train
    )

    if trained_nlp: print("\n--- Training process finished. ---")
    else: print("\n--- Training did not complete successfully. ---")
import os
import random
import json
import time
import requests
import signal # For handling signals like Ctrl+C gracefully
from concurrent.futures import ThreadPoolExecutor, as_completed # Import for concurrency

# --- Configuration --- (Keep this the same)
DATABASE_TYPE = "postgresql"
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "automation")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LexLuthern246!!??")

YOUR_FLASK_APP_URL = os.getenv("FLASK_APP_URL", "http://localhost:5000")
RECIPE_PROCESS_ENDPOINT = f"{YOUR_FLASK_APP_URL}/recipes/process-recipe"

TARGET_400_ERROR_RECIPES = 25
MAX_RECIPES_TO_SCAN_PER_BATCH = 500
MAX_TOTAL_RECIPES_TO_SCAN = 20000

OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES = "collected_instacart_400_error_recipes.json"
OUTPUT_FILE_COLLECTED_broken_RECIPES = "broken-recipes.json" # This will contain just the broken ingredient strings
OUTPUT_FILE_OTHER_ERRORS = "other_processing_errors.json"

# --- Concurrency Settings ---
MAX_WORKERS = 20 # Number of concurrent requests to make to your Flask app

# --- Database Connection Function (Keep this the same) ---
def get_db_connection():
    conn = None
    if DATABASE_TYPE == "postgresql":
        import psycopg2
        from psycopg2.extras import DictCursor
        try:
            conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            print("Successfully connected to PostgreSQL database.")
        except psycopg2.Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            return None
    else:
        print(f"Database type '{DATABASE_TYPE}' not configured.")
        raise NotImplementedError(f"DB connection for {DATABASE_TYPE} is not implemented.")
    return conn

# --- Fetch Recipes Function (Keep this the same) ---
def fetch_recipes_to_check(conn, num_recipes, already_processed_ids=None):
    recipes = []
    if not conn: return recipes
    if already_processed_ids is None: already_processed_ids = set()

    print(f"Fetching up to {num_recipes} new recipes from DB to check...")
    cursor = None
    try:
        if DATABASE_TYPE == "postgresql":
            from psycopg2.extras import DictCursor
            cursor = conn.cursor(cursor_factory=DictCursor)
            # Optimize WHERE IN clause for large sets of IDs to avoid very long query strings
            # If already_processed_ids is too large, it's better to just fetch random and filter in Python
            if 0 < len(already_processed_ids) < 5000: # Arbitrary threshold, adjust based on DB performance
                query = """
                        SELECT id, name, img_src, ingredients, instructions
                        FROM public.recipes
                        WHERE id NOT IN %s
                        ORDER BY RANDOM()
                            LIMIT %s;
                        """
                cursor.execute(query, (tuple(already_processed_ids), num_recipes))
            else:
                query = """
                        SELECT id, name, img_src, ingredients, instructions
                        FROM public.recipes
                        ORDER BY RANDOM()
                            LIMIT %s;
                        """
                cursor.execute(query, (num_recipes,))

            for row in cursor.fetchall():
                recipe_id = str(row["id"])
                if recipe_id not in already_processed_ids: # Double check in Python if DB query didn't exclude (e.g., if set too large)
                    ingredients = row["ingredients"] if isinstance(row["ingredients"], list) else []
                    instructions_raw = row["instructions"]
                    instructions = [instructions_raw] if isinstance(instructions_raw, str) else (instructions_raw if isinstance(instructions_raw, list) else [])
                    recipes.append({
                        "id": recipe_id, "title": row["name"],
                        "image_url": row.get("img_src", "") or "",
                        "ingredients": ingredients, "instructions": instructions

                    })
            print(f"Fetched {len(recipes)} new candidate recipes for this batch.")
    except Exception as e:
        print(f"Error fetching recipes: {e}")
    finally:
        if cursor: cursor.close()
    return recipes

# --- Function to save collected data ---
def save_collected_data(collected_recipes, other_errors, scanned_count, qualifying_count):
    print(f"\n--- Saving Collected Data ---")
    print(f"Target qualifying Instacart 400 errors (with empty name): {TARGET_400_ERROR_RECIPES}")
    print(f"Actual qualifying Instacart 400 errors collected so far: {qualifying_count}")
    print(f"Other processing errors logged so far: {len(other_errors)}")
    print(f"Total unique recipes scanned from DB in this run so far: {scanned_count}")

    # Process and save the broken ingredients
    if collected_recipes: # collected_recipes is the list of dictionaries
        broken_ingredients_list = []
        for recipe_data in collected_recipes:
            # Each recipe_data is a dictionary like { "recipe_id": ..., "line_items_with_empty_name_details": [...] }
            if 'line_items_with_empty_name_details' in recipe_data:
                for item_detail in recipe_data['line_items_with_empty_name_details']:
                    # Each item_detail is a dictionary like { "parsed_item_with_empty_name": ..., "broken-ingredient": "..." }
                    if 'broken-ingredient' in item_detail:
                        broken_ingredients_list.append(item_detail['broken-ingredient'])

        # Save the list of broken ingredient strings to broken-recipes.json
        try:
            with open(OUTPUT_FILE_COLLECTED_broken_RECIPES, 'w', encoding='utf-8') as f:
                json.dump(broken_ingredients_list, f, indent=2) # Dump as JSON array
            print(f"Broken ingredients saved to: {OUTPUT_FILE_COLLECTED_broken_RECIPES}")
        except Exception as e:
            print(f"ERROR writing broken ingredients file: {e}")

        # Save the full detailed collected 400-error recipes to collected_instacart_400_error_recipes.json
        try:
            with open(OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES, 'w', encoding='utf-8') as f:
                json.dump(collected_recipes, f, indent=2)
            print(f"Full details of collected 400-error recipes saved to: {OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES}")
        except Exception as e:
            print(f"ERROR writing full 400-error recipes details file: {e}") # Clarify error message

    # This message should only appear if no qualifying recipes were collected AND we actually scanned some
    elif scanned_count > 0:
        print(f"No recipes resulted in Instacart 400 errors with an empty ingredient name during this run (up to {scanned_count} scanned).")

    # Save other errors
    if other_errors:
        try:
            with open(OUTPUT_FILE_OTHER_ERRORS, 'w', encoding='utf-8') as f:
                json.dump(other_errors, f, indent=2)
            print(f"Details of other processing errors saved to: {OUTPUT_FILE_OTHER_ERRORS}")
        except Exception as e:
            print(f"ERROR writing other errors file: {e}")

# --- New function for concurrent processing of a single recipe ---
def process_recipe_concurrently(recipe):
    recipe_id_str = str(recipe.get('id', f'NO_ID_{random.randint(1000,9999)}'))
    recipe_title = recipe.get('title', 'Untitled Recipe')

    if not recipe.get("ingredients"):
        return {
            "type": "other_error",
            "data": {
                "recipe_id": recipe_id_str, "recipe_title": recipe_title,
                "error_type": "NoIngredientsInDB", "message": "Recipe from DB had no ingredients."
            }
        }

    payload = {
        "title": recipe_title,
        "image_url": recipe.get("image_url", ""),
        "ingredients": recipe.get("ingredients", []),
        "instructions": recipe.get("instructions", []),
        'link_type':'recipe'
    }

    try:
        session = requests.Session() # Use a session for potentially better performance over multiple calls
        response_from_flask = session.post(RECIPE_PROCESS_ENDPOINT, json=payload, timeout=30)
        # print(f"  Flask App HTTP Status for {recipe_id_str}: {response_from_flask.status_code}") # Optional: detailed print per recipe

        try:
            flask_response_data = response_from_flask.json()
        except json.JSONDecodeError:
            return {
                "type": "other_error",
                "data": {
                    "recipe_id": recipe_id_str, "recipe_title": recipe_title,
                    "error_type": "FlaskResponseNotJSON",
                    "flask_status_code": response_from_flask.status_code,
                    "flask_response_text": response_from_flask.text[:1000]
                }
            }

        instacart_api_status = flask_response_data.get("status_code")
        line_items_sent = flask_response_data.get("line_items", [])

        if instacart_api_status == 400:
            has_empty_name = False
            empty_name_ingredients_details = []
            if isinstance(line_items_sent, list):
                for i, item_sent in enumerate(line_items_sent):
                    if isinstance(item_sent, dict) and item_sent.get("name", "").strip() == "":
                        has_empty_name = True
                        empty_name_ingredients_details.append({
                            "parsed_item_with_empty_name": item_sent,
                            'index': i,
                            'broken-ingredient':payload['ingredients'][i] # This line is correct for adding the original string
                        })

            if has_empty_name:
                return {
                    "type": "collected_400_error",
                    "data": {
                        "recipe_id": recipe_id_str,
                        "recipe_title": recipe_title,
                        "original_ingredients_from_db": recipe.get("ingredients"),
                        "instacart_api_status_code": instacart_api_status,
                        "instacart_api_response_body": flask_response_data.get("response"),
                        "line_items_with_empty_name_details": empty_name_ingredients_details,
                        "all_line_items_sent_to_instacart": line_items_sent
                    }
                }
            else:
                return {
                    "type": "other_error",
                    "data": {
                        "recipe_id": recipe_id_str, "recipe_title": recipe_title,
                        "error_type": "Instacart400_NoEmptyNameDetected",
                        "original_ingredients_from_db": recipe.get("ingredients"),
                        "instacart_api_status_code": instacart_api_status,
                        "instacart_api_response_body": flask_response_data.get("response"),
                        "line_items_sent_to_instacart": line_items_sent
                    }
                }
        elif instacart_api_status is not None and instacart_api_status != 200:
            return {
                "type": "other_error",
                "data": {
                    "recipe_id": recipe_id_str, "recipe_title": recipe_title,
                    "error_type": "InstacartOtherError",
                    "original_ingredients_from_db": recipe.get("ingredients"),
                    "instacart_api_status_code": instacart_api_status,
                    "instacart_api_response_body": flask_response_data.get("response"),
                    "line_items_sent_to_instacart": line_items_sent
                }
            }
        else:
            # Successful 200 or other non-error status
            return {"type": "success", "recipe_id": recipe_id_str}

    except requests.exceptions.Timeout:
        return {"type": "other_error", "data": {"recipe_id": recipe_id_str, "recipe_title": recipe_title, "error_type": "FlaskRequestTimeout"}}
    except requests.exceptions.ConnectionError:
        # This is a critical error, often means Flask app is down
        return {"type": "critical_connection_error", "data": {"recipe_id": recipe_id_str, "recipe_title": recipe_title, "error_type": "FlaskConnectionError"}}
    except requests.exceptions.RequestException as e:
        return {"type": "other_error", "data": {"recipe_id": recipe_id_str, "recipe_title": recipe_title, "error_type": "FlaskRequestException", "message": str(e)}}
    except Exception as e:
        # Catch any other unexpected errors during processing
        return {"type": "other_error", "data": {"recipe_id": recipe_id_str, "recipe_title": recipe_title, "error_type": "UnexpectedErrorInWorker", "message": str(e)}}


# --- Main Function with Graceful Shutdown ---
def main():
    print(f"Starting Instacart 400 Error Collector. Goal: {TARGET_400_ERROR_RECIPES} recipes with Instacart 400 errors AND at least one empty ingredient name.")

    collected_recipes_with_empty_name_and_400_error = []
    other_processing_errors = []
    total_recipes_scanned_in_run = 0
    processed_recipe_ids_in_run = set()
    qualifying_400_errors_count = 0

    interrupted = False
    def signal_handler(sig, frame):
        nonlocal interrupted
        print("\nCtrl+C detected! Attempting to save data before exiting...")
        interrupted = True

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Using ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while qualifying_400_errors_count < TARGET_400_ERROR_RECIPES and \
                    total_recipes_scanned_in_run < MAX_TOTAL_RECIPES_TO_SCAN and \
                    not interrupted:

                print(f"\n--- Batch Start ---")
                print(f"Collected qualifying Instacart 400 errors (with empty name): {qualifying_400_errors_count}/{TARGET_400_ERROR_RECIPES}")
                print(f"Total unique recipes scanned in this run: {total_recipes_scanned_in_run}/{MAX_TOTAL_RECIPES_TO_SCAN}")

                db_conn = get_db_connection()
                if not db_conn:
                    print("DB connection failed. Waiting and retrying...")
                    if interrupted: break
                    time.sleep(10)
                    continue

                recipes_to_test_this_batch = fetch_recipes_to_check(db_conn, MAX_RECIPES_TO_SCAN_PER_BATCH, processed_recipe_ids_in_run)

                if db_conn:
                    if DATABASE_TYPE != "mongodb":
                        db_conn.close()

                if not recipes_to_test_this_batch:
                    print("No new recipes fetched. Pausing or ending.")
                    if interrupted: break
                    time.sleep(5)
                    if total_recipes_scanned_in_run > 0:
                        print("Exhausted new recipes or fetch_recipes_to_check needs refinement.")
                        break
                    continue

                futures = []
                recipes_submitted_to_flask_this_batch = 0 # Counter for recipes actually submitted to Flask

                for recipe in recipes_to_test_this_batch:
                    recipe_id_str = str(recipe.get('id', f'NO_ID_{random.randint(1000,9999)}'))
                    if recipe_id_str in processed_recipe_ids_in_run:
                        continue # Already processed this ID in a previous batch

                    processed_recipe_ids_in_run.add(recipe_id_str)
                    total_recipes_scanned_in_run += 1 # This counts recipes we *attempt* to process/consider

                    if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES or \
                            total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN or \
                            interrupted:
                        break # Stop submitting if targets met or interrupted

                    # Submit the recipe processing to the thread pool
                    futures.append(executor.submit(process_recipe_concurrently, recipe))
                    recipes_submitted_to_flask_this_batch += 1 # Increment for each task submitted

                print(f"  Submitted {recipes_submitted_to_flask_this_batch} recipes to Flask app for processing in this batch.")


                if not futures:
                    print("No valid recipes were submitted to Flask app in this batch (all skipped or targets met).")
                    if interrupted: break
                    continue

                recipes_completed_flask_processing_this_batch = 0 # Counter for recipes that completed Flask processing

                # Process results as they complete
                for future in as_completed(futures):
                    if interrupted:
                        print("Interrupted during result collection. Shutting down executor.")
                        # This causes remaining futures to be cancelled if possible, or wait until current task finishes
                        executor.shutdown(wait=False, cancel_futures=True)
                        break

                    try:
                        result = future.result() # Get the result from the completed task
                        recipes_completed_flask_processing_this_batch += 1 # Increment for any completed task

                        if result["type"] == "collected_400_error":
                            print(f"  COLLECTED (Instacart 400 & Empty Name): {result['data']['recipe_title']} (ID: {result['data']['recipe_id']})")

                            collected_recipes_with_empty_name_and_400_error.append(result["data"])
                            qualifying_400_errors_count += 1
                        elif result["type"] == "other_error":
                            error_data = result['data']
                            print(f"  LOGGED ({error_data['error_type']}): {error_data.get('recipe_title')} (ID: {error_data.get('recipe_id')})")
                            other_processing_errors.append(error_data)
                        elif result["type"] == "critical_connection_error":
                            error_data = result['data']
                            print(f"  CRITICAL ERROR ({error_data['error_type']}): {error_data.get('recipe_title')} (ID: {error_data.get('recipe_id')}) - Exiting.")
                            other_processing_errors.append(error_data)
                            interrupted = True # Trigger graceful shutdown
                            executor.shutdown(wait=False, cancel_futures=True) # Attempt to stop workers
                            break # Break from as_completed loop
                        # For "success" type, we don't need to do anything specific here, just count it implicitly in `total_recipes_scanned_in_run`

                    except Exception as exc:
                        print(f"  Error processing recipe result: {exc}")
                        other_processing_errors.append({"error_type": "ThreadPoolExecutionError", "message": str(exc)})

                print(f"  Completed processing for {recipes_completed_flask_processing_this_batch} recipes in this batch.") # Final print for batch completion


                if interrupted: break

                # Check if targets met after processing a batch of concurrent requests
                if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES or \
                        total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN:
                    break

                # No longer need a large sleep, as concurrency handles throughput
                # You might add a small sleep (e.g., 0.1s) if you notice your Flask app or Instacart API getting overloaded.
                # time.sleep(0.1)

    except Exception as e:
        print(f"UNEXPECTED ERROR in main loop: {e}")
    finally:
        print("\nReached finally block. Ensuring data is saved.")
        save_collected_data(
            collected_recipes_with_empty_name_and_400_error,
            other_processing_errors,
            total_recipes_scanned_in_run,
            qualifying_400_errors_count
        )
        print("\nScript finished or was interrupted.")

if __name__ == "__main__":
    main()
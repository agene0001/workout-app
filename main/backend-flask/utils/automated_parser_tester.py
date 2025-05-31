import os
import random
import json
import time
import requests
import signal # For handling signals like Ctrl+C gracefully

# --- Configuration --- (Keep this the same)
DATABASE_TYPE = "postgresql"
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "automation")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LexLuthern246!!??")

YOUR_FLASK_APP_URL = os.getenv("FLASK_APP_URL", "http://localhost:5000")
RECIPE_PROCESS_ENDPOINT = f"{YOUR_FLASK_APP_URL}/recipes/process-recipe"

TARGET_400_ERROR_RECIPES = 50
MAX_RECIPES_TO_SCAN_PER_BATCH = 500
MAX_TOTAL_RECIPES_TO_SCAN = 20000

OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES = "collected_instacart_400_error_recipes.json"
OUTPUT_FILE_OTHER_ERRORS = "other_processing_errors.json"

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
            if 0 < len(already_processed_ids) < 1000:
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
                if recipe_id not in already_processed_ids:
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

    if collected_recipes:
        titles_filename = OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES.replace(".json", "_titles.txt")
        details_filename = OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES # Keep for detailed JSON

        try:
            unique_titles = sorted(list(set(item["recipe_title"] for item in collected_recipes)))
            with open(titles_filename, 'w', encoding='utf-8') as f:
                for title in unique_titles:
                    f.write(f"{title}\n")
            print(f"Titles of collected recipes saved to: {titles_filename}")

            # Save detailed JSON
            with open(details_filename, 'w', encoding='utf-8') as f:
                json.dump(collected_recipes, f, indent=2)
            print(f"Full details of collected 400-error recipes saved to: {details_filename}")

        except Exception as e:
            print(f"ERROR writing collected 400-error recipes file: {e}")

    if other_errors:
        try:
            with open(OUTPUT_FILE_OTHER_ERRORS, 'w', encoding='utf-8') as f:
                json.dump(other_errors, f, indent=2)
            print(f"Details of other processing errors saved to: {OUTPUT_FILE_OTHER_ERRORS}")
        except Exception as e:
            print(f"ERROR writing other errors file: {e}")

    if not collected_recipes and scanned_count > 0:
        print(f"No recipes resulted in Instacart 400 errors with an empty ingredient name during this run (up to {scanned_count} scanned).")

# --- Main Function with Graceful Shutdown ---
def main():
    print(f"Starting Instacart 400 Error Collector. Goal: {TARGET_400_ERROR_RECIPES} recipes with Instacart 400 errors AND at least one empty ingredient name.")

    collected_recipes_with_empty_name_and_400_error = []
    other_processing_errors = []
    total_recipes_scanned_in_run = 0
    processed_recipe_ids_in_run = set()
    qualifying_400_errors_count = 0

    # Define a signal handler for Ctrl+C
    # This allows us to save data before exiting if the user interrupts.
    # Keep a flag to indicate if an interrupt occurred.
    interrupted = False
    def signal_handler(sig, frame):
        nonlocal interrupted # Use nonlocal to modify the flag in the outer scope
        print("\nCtrl+C detected! Attempting to save data before exiting...")
        interrupted = True

    signal.signal(signal.SIGINT, signal_handler) # Handle SIGINT (Ctrl+C)
    signal.signal(signal.SIGTERM, signal_handler) # Handle SIGTERM (kill command)


    try: # Main processing loop
        while qualifying_400_errors_count < TARGET_400_ERROR_RECIPES and \
                total_recipes_scanned_in_run < MAX_TOTAL_RECIPES_TO_SCAN and \
                not interrupted: # Check the interrupt flag

            print(f"\n--- Batch Start ---")
            print(f"Collected qualifying Instacart 400 errors (with empty name): {qualifying_400_errors_count}/{TARGET_400_ERROR_RECIPES}")
            print(f"Total unique recipes scanned in this run: {total_recipes_scanned_in_run}/{MAX_TOTAL_RECIPES_TO_SCAN}")

            db_conn = get_db_connection()
            if not db_conn:
                print("DB connection failed. Waiting and retrying...")
                if interrupted: break # Don't sleep if already interrupted
                time.sleep(10)
                continue

            recipes_to_test_this_batch = fetch_recipes_to_check(db_conn, MAX_RECIPES_TO_SCAN_PER_BATCH, processed_recipe_ids_in_run)

            if db_conn:
                if DATABASE_TYPE != "mongodb": # Assuming mongodb has different close logic
                    db_conn.close()

            if not recipes_to_test_this_batch:
                print("No new recipes fetched. Pausing or ending.")
                if interrupted: break
                time.sleep(5)
                if total_recipes_scanned_in_run > 0: # Check if we actually tried and got nothing new
                    print("Exhausted new recipes or fetch_recipes_to_check needs refinement.")
                    break # Exit loop if no new recipes after processing some
                continue

            for recipe in recipes_to_test_this_batch:
                if interrupted: break # Check before processing each recipe

                recipe_id_str = str(recipe.get('id', f'NO_ID_{random.randint(1000,9999)}'))
                if recipe_id_str in processed_recipe_ids_in_run:
                    continue

                if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES or \
                        total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN:
                    break # Break inner loop if targets met

                processed_recipe_ids_in_run.add(recipe_id_str)
                total_recipes_scanned_in_run += 1

                print(f"\n({qualifying_400_errors_count} collected) ({total_recipes_scanned_in_run} scanned) Processing Recipe ID: {recipe_id_str}, Title: {recipe.get('title')}")

                payload = {
                    "title": recipe.get("title", "Untitled Recipe"),
                    "image_url": recipe.get("image_url", ""),
                    "ingredients": recipe.get("ingredients", []),
                    "instructions": recipe.get("instructions", []),
                    'link_type':'recipe'
                }
                if not payload["ingredients"]:
                    print("  Skipping recipe: No ingredients found.")
                    other_processing_errors.append({
                        "recipe_id": recipe_id_str, "recipe_title": recipe.get("title"),
                        "error_type": "NoIngredientsInDB", "message": "Recipe from DB had no ingredients."
                    })
                    continue

                try:
                    response_from_flask = requests.post(RECIPE_PROCESS_ENDPOINT, json=payload, timeout=30)
                    print(f"  Flask App HTTP Status to Tester: {response_from_flask.status_code}")
                    try:
                        flask_response_data = response_from_flask.json()
                    except json.JSONDecodeError:
                        print(f"  ERROR: Flask response not JSON. Status: {response_from_flask.status_code}. Text: {response_from_flask.text[:200]}")
                        other_processing_errors.append({
                            "recipe_id": recipe_id_str, "recipe_title": recipe.get("title"),
                            "error_type": "FlaskResponseNotJSON",
                            "flask_status_code": response_from_flask.status_code,
                            "flask_response_text": response_from_flask.text[:1000]
                        })
                        continue
                    instacart_api_status = flask_response_data.get("status_code")
                    line_items_sent = flask_response_data.get("line_items", [])

                    if instacart_api_status == 400:
                        has_empty_name = False
                        empty_name_ingredients_details = [] # Renamed for clarity
                        if isinstance(line_items_sent, list):
                            for i in range(len(line_items_sent)): # Renamed for clarity
                                # print(item_sent.get("name", "").strip())
                                if isinstance(line_items_sent[i], dict) and line_items_sent[i].get("name", "").strip() == "":
                                    has_empty_name = True
                                    # Try to find the original ingredient line that led to this empty name
                                    # This requires your Flask app to return more info or a more robust matching here.
                                    # For now, we'll just store the problematic parsed item.
                                    empty_name_ingredients_details.append({
                                        "parsed_item_with_empty_name": line_items_sent[i],
                                        'index': i
                                    })

                        if has_empty_name:
                            print(f"  COLLECTED (Instacart 400 & Empty Name): Status {instacart_api_status} for Recipe: {recipe.get('title')}")
                            collected_recipes_with_empty_name_and_400_error.append({
                                "recipe_id": recipe_id_str,
                                "recipe_title": recipe.get("title"),
                                "original_ingredients_from_db": recipe.get("ingredients"),
                                "instacart_api_status_code": instacart_api_status,
                                "instacart_api_response_body": flask_response_data.get("response"),
                                "line_items_with_empty_name_details": empty_name_ingredients_details,
                                "all_line_items_sent_to_instacart": line_items_sent
                            })
                            qualifying_400_errors_count += 1
                        else:
                            print(f"  LOGGED (Instacart 400, but no empty name detected in parsed items): Status {instacart_api_status} for Recipe: {recipe.get('title')}")
                            other_processing_errors.append({
                                "recipe_id": recipe_id_str, "recipe_title": recipe.get("title"),
                                "error_type": "Instacart400_NoEmptyNameDetected",
                                "original_ingredients_from_db": recipe.get("ingredients"),
                                "instacart_api_status_code": instacart_api_status,
                                "instacart_api_response_body": flask_response_data.get("response"),
                                "line_items_sent_to_instacart": line_items_sent
                            })
                    elif instacart_api_status is not None and instacart_api_status != 200:
                        print(f"  LOGGED (Other Instacart API Error): Status {instacart_api_status} for Recipe: {recipe.get('title')}")
                        other_processing_errors.append({
                            "recipe_id": recipe_id_str, "recipe_title": recipe.get("title"),
                            "error_type": "InstacartOtherError",
                            "original_ingredients_from_db": recipe.get("ingredients"),
                            "instacart_api_status_code": instacart_api_status,
                            "instacart_api_response_body": flask_response_data.get("response"),
                            "line_items_sent_to_instacart": line_items_sent
                        })

                except requests.exceptions.Timeout:
                    print(f"  ERROR: Request to Flask app timed out for recipe {recipe_id_str}.")
                    other_processing_errors.append({"recipe_id": recipe_id_str, "recipe_title": recipe.get("title"), "error_type": "FlaskRequestTimeout"})
                except requests.exceptions.ConnectionError:
                    print(f"  ERROR: Could not connect to Flask app at {RECIPE_PROCESS_ENDPOINT}. Is it running?")
                    other_processing_errors.append({"recipe_id": recipe_id_str, "recipe_title": recipe.get("title"), "error_type": "FlaskConnectionError"})
                    print("  Exiting script as Flask app seems unavailable.")
                    interrupted = True # Treat this as an interrupt to trigger save
                    break # Break from inner loop
                except requests.exceptions.RequestException as e:
                    print(f"  ERROR calling Flask app for recipe {recipe_id_str}: {e}")
                    other_processing_errors.append({"recipe_id": recipe_id_str, "recipe_title": recipe.get("title"), "error_type": "FlaskRequestException", "message": str(e)})

                if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES or \
                        total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN:
                    break # Break inner loop

            if interrupted: break # Break outer loop if interrupted

            # Check if targets met after processing a batch
            if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES or \
                    total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN or \
                    (not recipes_to_test_this_batch and total_recipes_scanned_in_run > 0): # No new recipes and we've processed some
                break # Break outer loop

            if not interrupted: # Don't sleep if we're trying to exit quickly
                time.sleep(0.2)

    except Exception as e: # Catch any other unexpected errors in the main loop
        print(f"UNEXPECTED ERROR in main loop: {e}")
        # This will fall through to the finally block
    finally:
        # This block will execute whether the try block completed normally,
        # // an exception occurred, or a signal was caught (if the signal handler doesn't exit directly).
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
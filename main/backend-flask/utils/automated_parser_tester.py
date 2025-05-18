import os
import random
import json
import time
import requests

# --- Configuration ---
DATABASE_TYPE = "postgresql"
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "automation")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "LexLuthern246!!??") # Use env var in prod

YOUR_FLASK_APP_URL = os.getenv("FLASK_APP_URL", "http://localhost:5000")
RECIPE_PROCESS_ENDPOINT = f"{YOUR_FLASK_APP_URL}/recipes/process-recipe"

TARGET_400_ERROR_RECIPES = 50      # How many recipes resulting in Instacart 400 errors to collect
MAX_RECIPES_TO_SCAN_PER_BATCH = 50 # How many recipes to fetch from DB in each batch
MAX_TOTAL_RECIPES_TO_SCAN = 1000   # Safety limit

OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES = "collected_instacart_400_error_recipes.json"
OUTPUT_FILE_OTHER_ERRORS = "other_processing_errors.json" # For Flask errors or non-400 Instacart errors

# --- Database Connection Function (Implement for your DB) ---
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

# --- Fetch Recipes Function (Adapt or replace) ---
def fetch_recipes_to_check(conn, num_recipes, already_processed_ids=None):
    """
    Fetches recipes to test, attempting to avoid those already processed in this run.
    """
    recipes = []
    if not conn: return recipes
    if already_processed_ids is None: already_processed_ids = set()

    print(f"Fetching up to {num_recipes} new recipes from DB to check...")
    cursor = None
    try:
        if DATABASE_TYPE == "postgresql":
            from psycopg2.extras import DictCursor
            cursor = conn.cursor(cursor_factory=DictCursor)
            # Exclude already processed IDs if the set is not too large for an IN clause
            # For very large sets, other strategies might be needed (e.g., temp table)
            # For simplicity, if too many, we might just rely on RANDOM() to eventually get new ones.
            if 0 < len(already_processed_ids) < 1000: # Avoid huge IN clauses
                query = """
                        SELECT id, name, img_src, ingredients, instructions
                        FROM public.recipes
                        WHERE id NOT IN %s
                        ORDER BY RANDOM()
                            LIMIT %s; \
                        """
                cursor.execute(query, (tuple(already_processed_ids), num_recipes))
            else:
                query = """
                        SELECT id, name, img_src, ingredients, instructions
                        FROM public.recipes
                        ORDER BY RANDOM()
                            LIMIT %s; \
                        """
                cursor.execute(query, (num_recipes,))

            for row in cursor.fetchall():
                recipe_id = str(row["id"])
                if recipe_id not in already_processed_ids: # Double check, though query should handle
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
def main():
    print(f"Starting Instacart 400 Error Collector. Goal: {TARGET_400_ERROR_RECIPES} recipes with Instacart 400 errors AND at least one empty ingredient name.")

    collected_recipes_with_empty_name_and_400_error = [] # This will store the desired recipe info
    other_processing_errors = []

    total_recipes_scanned_in_run = 0
    processed_recipe_ids_in_run = set()

    # Keep track of how many *qualifying* 400 errors we've found
    qualifying_400_errors_count = 0

    while qualifying_400_errors_count < TARGET_400_ERROR_RECIPES and \
            total_recipes_scanned_in_run < MAX_TOTAL_RECIPES_TO_SCAN:

        print(f"\n--- Batch Start ---")
        print(f"Collected qualifying Instacart 400 errors (with empty name): {qualifying_400_errors_count}/{TARGET_400_ERROR_RECIPES}")
        print(f"Total unique recipes scanned in this run: {total_recipes_scanned_in_run}/{MAX_TOTAL_RECIPES_TO_SCAN}")

        db_conn = get_db_connection()
        if not db_conn:
            print("DB connection failed. Waiting and retrying...")
            time.sleep(10)
            continue

        recipes_to_test_this_batch = fetch_recipes_to_check(db_conn, MAX_RECIPES_TO_SCAN_PER_BATCH, processed_recipe_ids_in_run)

        if db_conn: # Ensure connection is closed if it was opened
            if DATABASE_TYPE != "mongodb":
                db_conn.close()
            # For MongoDB, client closing might be handled differently or at script end

        if not recipes_to_test_this_batch:
            print("No new recipes fetched. Pausing or ending.")
            time.sleep(5)
            if total_recipes_scanned_in_run > 0 and not recipes_to_test_this_batch :
                print("Exhausted new recipes or fetch_recipes_to_check needs refinement.")
                break
            continue

        for recipe in recipes_to_test_this_batch:
            recipe_id_str = str(recipe.get('id', f'NO_ID_{random.randint(1000,9999)}'))

            if recipe_id_str in processed_recipe_ids_in_run:
                continue

            if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES:
                print("Target number of qualifying Instacart 400 error recipes reached. Stopping.")
                break
            if total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN:
                print("Maximum total recipes to scan reached. Stopping.")
                break

            processed_recipe_ids_in_run.add(recipe_id_str)
            total_recipes_scanned_in_run += 1

            print(f"\n({qualifying_400_errors_count} collected) ({total_recipes_scanned_in_run} scanned) Processing Recipe ID: {recipe_id_str}, Title: {recipe.get('title')}")

            payload = {
                "title": recipe.get("title", "Untitled Recipe"),
                "image_url": recipe.get("image_url", ""),
                "ingredients": recipe.get("ingredients", []),
                "instructions": recipe.get("instructions", [])
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
                line_items_sent = flask_response_data.get("processed_ingredients", [])

                # --- MODIFIED LOGIC HERE ---
                if instacart_api_status == 400:
                    has_empty_name = False
                    empty_name_ingredients = []
                    if isinstance(line_items_sent, list): # Ensure it's a list
                        for item in line_items_sent:
                            if isinstance(item, dict) and item.get("name", "").strip() == "":
                                has_empty_name = True
                                empty_name_ingredients.append({
                                    "original_line_text_if_available": "N/A - requires Flask to send original line per parsed item", # See note below
                                    "parsed_item_with_empty_name": item
                                })

                    if has_empty_name:
                        print(f"  COLLECTED (Instacart 400 & Empty Name): Status {instacart_api_status} for Recipe: {recipe.get('title')}")
                        collected_recipes_with_empty_name_and_400_error.append({
                            "recipe_id": recipe_id_str,
                            "recipe_title": recipe.get("title"),
                            "original_ingredients_from_db": recipe.get("ingredients"), # The full original list
                            "instacart_api_status_code": instacart_api_status,
                            "instacart_api_response_body": flask_response_data.get("response"),
                            "line_items_with_empty_name_details": empty_name_ingredients,
                            "all_line_items_sent_to_instacart": line_items_sent
                        })
                        qualifying_400_errors_count += 1
                    else:
                        # It was a 400 error, but not due to an empty name we could detect here. Log it elsewhere.
                        print(f"  LOGGED (Instacart 400, but no empty name detected in parsed items): Status {instacart_api_status} for Recipe: {recipe.get('title')}")
                        other_processing_errors.append({
                            "recipe_id": recipe_id_str, "recipe_title": recipe.get("title"),
                            "error_type": "Instacart400_NoEmptyNameDetected",
                            "original_ingredients_from_db": recipe.get("ingredients"),
                            "instacart_api_status_code": instacart_api_status,
                            "instacart_api_response_body": flask_response_data.get("response"),
                            "line_items_sent_to_instacart": line_items_sent
                        })
                elif instacart_api_status != 200: # Other non-200, non-400 Instacart errors
                    print(f"  LOGGED (Other Instacart API Error): Status {instacart_api_status} for Recipe: {recipe.get('title')}")
                    other_processing_errors.append({
                        "recipe_id": recipe_id_str, "recipe_title": recipe.get("title"),
                        "error_type": "InstacartOtherError",
                        "original_ingredients_from_db": recipe.get("ingredients"),
                        "instacart_api_status_code": instacart_api_status,
                        "instacart_api_response_body": flask_response_data.get("response"),
                        "line_items_sent_to_instacart": line_items_sent
                    })
                # else: # Instacart API call was 200 OK - not logging these to a file

            except requests.exceptions.Timeout:
                print(f"  ERROR: Request to Flask app timed out for recipe {recipe_id_str}.")
                other_processing_errors.append({"recipe_id": recipe_id_str, "recipe_title": recipe.get("title"), "error_type": "FlaskRequestTimeout"})
            except requests.exceptions.ConnectionError:
                print(f"  ERROR: Could not connect to Flask app at {RECIPE_PROCESS_ENDPOINT}. Is it running?")
                other_processing_errors.append({"recipe_id": recipe_id_str, "recipe_title": recipe.get("title"), "error_type": "FlaskConnectionError"})
                print("  Exiting script as Flask app seems unavailable.")
                break
            except requests.exceptions.RequestException as e:
                print(f"  ERROR calling Flask app for recipe {recipe_id_str}: {e}")
                other_processing_errors.append({"recipe_id": recipe_id_str, "recipe_title": recipe.get("title"), "error_type": "FlaskRequestException", "message": str(e)})

            if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES: break
            if total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN: break

        if qualifying_400_errors_count >= TARGET_400_ERROR_RECIPES or \
                total_recipes_scanned_in_run >= MAX_TOTAL_RECIPES_TO_SCAN or \
                (not recipes_to_test_this_batch and total_recipes_scanned_in_run > 0):
            break

        time.sleep(0.2)

    print(f"\n--- Collection Summary ---")
    print(f"Target qualifying Instacart 400 errors (with empty name): {TARGET_400_ERROR_RECIPES}")
    print(f"Actual qualifying Instacart 400 errors collected: {qualifying_400_errors_count}")
    print(f"Other processing errors logged: {len(other_processing_errors)}")
    print(f"Total unique recipes scanned from DB in this run: {total_recipes_scanned_in_run}")

    if collected_recipes_with_empty_name_and_400_error:
        # Change to write just titles, one per line
        with open(OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES.replace(".json", "_titles.txt"), 'w', encoding='utf-8') as f:
            unique_titles = sorted(list(set(item["recipe_title"] for item in collected_recipes_with_empty_name_and_400_error)))
            for title in unique_titles:
                f.write(f"{title}\n")
        print(f"Titles of recipes with Instacart 400 errors AND empty ingredient names saved to: {OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES.replace('.json', '_titles.txt')}")

    #     # Optionally, still save the detailed JSON for these specific cases if useful for deeper debugging
    #     with open(OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES, 'w', encoding='utf-8') as f:
    #         json.dump(collected_recipes_with_empty_name_and_400_error, f, indent=2)
    #     print(f"Full details of these recipes saved to: {OUTPUT_FILE_COLLECTED_400_ERROR_RECIPES}")
    #
    # if other_processing_errors:
    #     with open(OUTPUT_FILE_OTHER_ERRORS, 'w', encoding='utf-8') as f:
    #         json.dump(other_processing_errors, f, indent=2)
    #     print(f"Details of other processing errors saved to: {OUTPUT_FILE_OTHER_ERRORS}")

    if not collected_recipes_with_empty_name_and_400_error and total_recipes_scanned_in_run > 0:
        print(f"No recipes resulted in Instacart 400 errors with an empty ingredient name during this run (up to {total_recipes_scanned_in_run} scanned).")

    print("\nScript finished.")

if __name__ == "__main__":
    main()
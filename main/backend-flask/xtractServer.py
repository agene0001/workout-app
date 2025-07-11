import requests
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
import traceback # For detailed error logging

# Ensure your NER model/parser is correctly imported
# These imports are critical for your app's functionality.
# The health check will attempt to verify their presence and basic functionality.
try:
    from utils.NERModel.ingredient_parser import extract_ingredients_ner, parse_fraction
    NER_MODEL_IMPORTED = True
except ImportError as e:
    NER_MODEL_IMPORTED = False
    NER_MODEL_IMPORT_ERROR = str(e)
    print(f"CRITICAL ERROR: Failed to import NER model components: {e}")
    traceback.print_exc()
load_dotenv()
recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

instacart_env = os.getenv("NODE_ENV", "dev")
def process_recipe_for_instacart(
        title: str,
        link_type: str,
        ingredients_input_data, # Can be List[str] for 'recipe' or List[CartItem-like dict] for 'shopping_list'
        instructions: list = None,
        image_url: str = "",
        landing_page_config: dict = None
):
    """
    Processes ingredients based on link_type and generates an Instacart link.
    The Python NER parser is the single source of truth for parsing raw ingredient strings.
    """
    final_instacart_line_items = []
    api_key = os.getenv("INSTACART_API_KEY")

    if not api_key:
        print("ERROR: INSTACART_API_KEY not found.")
        return {"status_code": 500, "response": {"error": "Server configuration error: API key missing."}}

    if link_type == 'recipe':
        if not (isinstance(ingredients_input_data, list) and all(isinstance(i, str) for i in ingredients_input_data)):
            msg = "For 'recipe' link_type, 'ingredients' must be a list of raw strings."
            print(f"ERROR: {msg} Got: {type(ingredients_input_data)}")
            return {"status_code": 400, "response": {"error": msg}}

        # Python NER parses raw strings for a single recipe
        final_instacart_line_items = extract_ingredients_ner(ingredients_input_data)
        if not instructions: # Default instructions for recipes
            instructions = ["Follow recipe steps.", "Enjoy your meal!"]

    elif link_type == 'shopping_list':
        if not (isinstance(ingredients_input_data, list) and all(isinstance(i, dict) for i in ingredients_input_data)):
            msg = "For 'shopping_list' link_type, 'ingredients' (cart data) must be a list of item dictionaries."
            print(f"ERROR: {msg} Got: {type(ingredients_input_data)}")
            return {"status_code": 400, "response": {"error": msg}}

        aggregated_for_instacart = {} # To aggregate items by name|unit

        for cart_item_data in ingredients_input_data:
            item_type = cart_item_data.get('type')

            if item_type == 'recipe_batch':
                recipe_details = cart_item_data.get('recipe', {})
                raw_ingredients = recipe_details.get('ingredients', [])
                servings = float(cart_item_data.get('servingsMultiplier', 1))
                if not servings > 0: servings = 1

                if not (isinstance(raw_ingredients, list) and all(isinstance(i, str) for i in raw_ingredients)):
                    print(f"Warning: Skipping recipe batch due to invalid ingredients format: {recipe_details.get('recipeName')}")
                    continue

                # Python NER parses raw strings for this recipe batch
                parsed_base_ingredients = extract_ingredients_ner(raw_ingredients)

                for parsed_ing in parsed_base_ingredients:
                    try:
                        # Attempt to convert quantity to float for scaling
                        # Your `extract_ingredients_ner` might return quantity as str or num.
                        # `parse_fraction` can help standardize this.
                        base_qty_str = str(parsed_ing.get('quantity', '1')).strip()
                        base_qty_num = 1.0
                        if base_qty_str:
                            parsed_val = parse_fraction(base_qty_str) # Use your robust fraction/number parser
                            if parsed_val is not None:
                                base_qty_num = parsed_val
                            else: # Could not parse quantity string, default to 1 or log error
                                print(f"Warning: Could not parse quantity '{base_qty_str}' for '{parsed_ing.get('name')}'. Defaulting to 1.")

                        scaled_qty = base_qty_num * servings
                        if scaled_qty <= 0: continue # Skip if scaled quantity is zero or less

                        unit = str(parsed_ing.get('unit', 'each')).lower().strip() or 'each'
                        name = str(parsed_ing.get('name', '')).strip()
                        if not name: continue # Skip if no name after parsing

                        # Key for aggregation
                        agg_key = f"{name.lower()}|{unit}"

                        if agg_key in aggregated_for_instacart:
                            aggregated_for_instacart[agg_key]['quantity'] += scaled_qty
                        else:
                            aggregated_for_instacart[agg_key] = {
                                'name': name,
                                'quantity': scaled_qty,
                                'unit': unit,
                                'display_text': parsed_ing.get('display_text', name) # Original parsed display_text
                            }
                    except Exception as e_scale:
                        print(f"Error scaling/processing ingredient '{parsed_ing}': {e_scale}")
                        traceback.print_exc()


            elif item_type == 'custom_standalone_ingredient':
                name = str(cart_item_data.get('name', '')).strip()
                if not name: continue

                qty = float(cart_item_data.get('quantity', 1))
                if qty <= 0: continue

                unit = str(cart_item_data.get('unit', 'each')).lower().strip() or 'each'

                agg_key = f"{name.lower()}|{unit}"
                if agg_key in aggregated_for_instacart:
                    aggregated_for_instacart[agg_key]['quantity'] += qty
                else:
                    aggregated_for_instacart[agg_key] = {
                        'name': name,
                        'quantity': qty,
                        'unit': unit,
                        'display_text': name # For custom items, name is display_text
                    }
            else:
                print(f"Warning: Unknown cart item type '{item_type}'. Skipping.")

        final_instacart_line_items = list(aggregated_for_instacart.values())
        instructions = None # No instructions for a master shopping list typically

    else:
        return {"status_code": 400, "response": {"error": f"Invalid link_type: {link_type}"}}

    if not final_instacart_line_items:
        return {"status_code": 400, "response": {"error": "No valid line items to send to Instacart."}}
    landing_page_config = {"partner_linkback_url":"https://gainztrackers.com/order-success",}
    # Construct Instacart payload
    payload = {
        "title": title,
        "link_type": link_type,
        "line_items": final_instacart_line_items,
        'landing_page_configuration':landing_page_config

    }
    if image_url: payload["image_url"] = image_url
    if instructions: payload["instructions"] = instructions # Only for 'recipe' usually

    # if link_type == 'recipe':
        # payload["expires_in"] = 30
        # default_recipe_landing_config = {"enable_pantry_items": True}
        # payload["landing_page_configuration"] = landing_page_config if landing_page_config else default_recipe_landing_config
    # else: # shopping_list
        # payload["expires_in"] = 7 # Or configurable
        # if landing_page_config: payload["landing_page_configuration"] = landing_page_config

    print("Final Instacart Payload:", payload)

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    api_url_base = "https://connect.instacart.com"
    if instacart_env == "dev":
    # add this once we get the api key to use
        api_url_base = "https://connect.dev.instacart.tools"
    api_url = f"{api_url_base}/idp/v1/products/products_link"

    response_data = None
    status_code = 500
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=15)
        status_code = response.status_code
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err} - Status: {status_code} - Response: {response.text if response else 'N/A'}")
        try:
            response_data = response.json() if response and response.headers.get('Content-Type') == 'application/json' else {"error": str(http_err), "details_text": response.text if response else None}
        except ValueError:
            response_data = {"error": "Instacart API HTTP error (non-JSON)", "details_text": response.text if response else None}
    except requests.exceptions.Timeout:
        print("Instacart API timed out.")
        response_data = {"error": "Instacart API request timed out."}
        status_code = 504
    except requests.exceptions.RequestException as err:
        print(f"Instacart API request error: {err}")
        response_data = {"error": f"Could not connect to Instacart API: {err}"}
    except ValueError: # JSONDecodeError
        print("Instacart API response was not valid JSON.")
        response_data = {"error": "Invalid JSON response from Instacart API."}



    return {
        "status_code": status_code,
        "response": response_data,
        "line_items": final_instacart_line_items, # <--- ADD THIS LINE

        # For debugging, you might want to return what was sent if link_type was 'recipe'
        "sent_line_items_count": len(final_instacart_line_items)
    }

@recipe_bp.route('/process-recipe', methods=['POST'])
def process_recipe_api_route(): # Renamed to avoid conflict with the function
    try:
        data = request.json
        if not data: return jsonify({"error": "Request body must be JSON"}), 400

        link_type = data.get("link_type")
        if not link_type or link_type not in ['recipe', 'shopping_list']:
            return jsonify({"error": "Missing or invalid 'link_type'. Must be 'recipe' or 'shopping_list'."}), 400

        title = data.get('title')
        if not title: return jsonify({"error": "Missing 'title' field"}), 400

        # 'ingredients' field now holds:
        # - List[str] for 'recipe'
        # - List[CartItem-like dict] for 'shopping_list'
        ingredients_input_data = data.get('ingredients')
        if ingredients_input_data is None:
            return jsonify({"error": "Missing 'ingredients' field"}), 400
        print(ingredients_input_data)
        instructions = data.get('instructions')
        image_url = data.get('image_url', '')
        landing_page_config = data.get('landing_page_configuration')

        result = process_recipe_for_instacart( # Call the refactored function
            title=title,
            link_type=link_type,
            ingredients_input_data=ingredients_input_data,
            instructions=instructions,
            image_url=image_url,
            # landing_page_config=landing_page_config
        )
        if instacart_env != 'dev':
            result['response']['products_link_url']+="?utm_campaign=instacart-idp&utm_medium=affiliate&utm_source=instacart_idp&utm_term=partnertype-mediapartner&utm_content=campaignid-20313_partnerid-6170383"

        return jsonify(result), result.get("status_code", 500)

    except Exception as e:
        print(f"Error in /process-recipe endpoint: {e}")
        traceback.print_exc() # Print full traceback for server-side debugging
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

# Rest of your app.py (health check, app registration, main execution block)
# ... (make sure these are present and correct as per your original file)
app = Flask(__name__) # Ensure app is defined before registering blueprint
CORS(app)
app.register_blueprint(recipe_bp)

# --- Health Check additions ---

def check_instacart_api_connectivity():
    """Attempts a lightweight GET request to the Instacart API base URL to check connectivity."""
    api_url_base = "https://connect.instacart.com"
    if os.getenv("NODE_ENV", "dev") == "dev":
        api_url_base = "https://connect.dev.instacart.tools" # Use dev endpoint for dev env

    try:
        # Attempt to reach the base URL. A GET to the root might not be a valid API endpoint,
        # but it checks DNS resolution and basic network connectivity.
        # For a more robust check, you might ping a known public, lightweight API endpoint
        # provided by Instacart for health checks if one exists.
        response = requests.get(api_url_base, timeout=5) # Reduced timeout for health check
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return {"status": "ok", "message": f"Successfully connected to {api_url_base}"}
    except requests.exceptions.Timeout:
        return {"status": "timeout", "message": f"Connection to Instacart API timed out ({api_url_base})."}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": f"Could not connect to Instacart API ({api_url_base}). Verify network or API availability."}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "message": f"Instacart API returned HTTP error: {e.response.status_code} at {api_url_base}. Response: {e.response.text}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error checking Instacart API: {str(e)}"}


app = Flask(__name__) # Ensure app is defined before registering blueprint
CORS(app)
app.register_blueprint(recipe_bp)

@app.route('/health', methods=['GET'])
def health_check():
    health_status = {
        "status": "healthy", # Assume healthy unless a check fails
        "details": {}
    }
    overall_ok = True # Flag to track overall health

    # 1. Check Environment Variables
    instacart_api_key_present = bool(os.getenv("INSTACART_API_KEY"))
    health_status["details"]["instacart_api_key"] = {
        "status": "ok" if instacart_api_key_present else "missing",
        "message": "Instacart API Key is present." if instacart_api_key_present else "Instacart API Key is MISSING. Core functionality may be impacted."
    }
    if not instacart_api_key_present:
        overall_ok = False

    # 2. Check NER Model availability and basic functionality
    ner_model_functional = False
    ner_model_message = "NER model (ingredient_parser) is not imported." # Default if import failed
    if NER_MODEL_IMPORTED:
        try:
            # Attempt a very basic call to ensure it's functional, not just imported.
            # This assumes extract_ingredients_ner can handle an empty list or simple string without crashing.
            test_ingredients = ["1 cup flour", "2 eggs"]
            parsed_test = extract_ingredients_ner(test_ingredients)
            fraction_test = parse_fraction("3/4")
            if parsed_test is not None and isinstance(parsed_test, list) and fraction_test is not None:
                ner_model_functional = True
                ner_model_message = "NER model (ingredient_parser) imported and passed basic functionality test."
            else:
                ner_model_message = "NER model (ingredient_parser) imported but failed basic functionality test."
                print(f"WARNING: {ner_model_message} - Parsed: {parsed_test}, Fraction: {fraction_test}")
        except Exception as e:
            ner_model_message = f"NER model (ingredient_parser) imported but crashed during basic functionality test: {str(e)}"
            print(f"ERROR: {ner_model_message}")
            traceback.print_exc() # Print full traceback for server-side debugging
    else:
        ner_model_message = f"NER model (ingredient_parser) failed to import at startup: {NER_MODEL_IMPORT_ERROR}"

    health_status["details"]["ner_model"] = {
        "status": "ok" if ner_model_functional else "error",
        "message": ner_model_message
    }
    if not ner_model_functional:
        overall_ok = False

    # 3. Check Instacart API Connectivity
    instacart_connectivity_check = check_instacart_api_connectivity()
    health_status["details"]["instacart_api_connectivity"] = instacart_connectivity_check
    if instacart_connectivity_check["status"] != "ok":
        overall_ok = False

    # Set overall status and HTTP code based on checks
    if not overall_ok:
        health_status["status"] = "unhealthy"
        return jsonify(health_status), 503 # Service Unavailable
    else:
        return jsonify(health_status), 200 # OK

if __name__ == "__main__":
    host_env = os.getenv("NODE_ENV", "dev")
    port = 5000
    if host_env == "production":
        port = int(os.getenv("PORT", 8082))
        app.run(debug=False, host='0.0.0.0', port=port)
    elif host_env == 'dev':
        port = int(os.getenv("PORT", 5000))
        app.run(debug=True, host='0.0.0.0', port=port)
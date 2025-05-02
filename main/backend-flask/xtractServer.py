import requests

from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

from utils.ingredient_utils import extract_ingredients

# Load environment variables
load_dotenv()

# Initialize Flask app
recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')
# Load small English model

# --- Flask App Code (unchanged from your example) ---

def process_recipe(ingredients_list, instructions, title, image_url=""):
    """Process recipe ingredients and instructions and send to Instacart API"""
    # Extract ingredients
    parsed_ingredients = extract_ingredients(ingredients_list)

    # Build payload for POST request
    payload = {
        "title": title,
        "image_url": image_url,
        "expires_in": 1,
        "instructions": instructions,
        "line_items": parsed_ingredients
    }
    print(payload)
    # Get API key from environment
    api_key = os.getenv("API_KEY")

    # Debug log (remove in production)

    headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    response = requests.post(
        "https://connect.dev.instacart.tools/idp/v1/products/products_link",
        headers=headers,
        json=payload
    )
    try:
        data = response.json()
    except ValueError:
        print("Response was not valid JSON.")
        data = None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
        data = None
    except requests.exceptions.Timeout:
        print("The request timed out.")
        data = None
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        data = None

    return {
        "status_code": response.status_code,
        "response": data,
        "processed_ingredients": parsed_ingredients
    }


app = Flask(__name__)
CORS(app)

@recipe_bp.route('/process-recipe', methods=['POST'])
def process_recipe_api():
    try:
        data = request.json
        if not data: return jsonify({"error": "Request body must be JSON"}), 400
        if 'title' not in data: return jsonify({"error": "Missing title field"}), 400
        if 'ingredients' not in data: return jsonify({"error": "Missing ingredients field"}), 400
        if 'instructions' not in data: return jsonify({"error": "Missing instructions field"}), 400

        title = data.get('title', 'Recipe')
        image_url = data.get('image_url', '')

        result = process_recipe(
            data['ingredients'], data['instructions'], title, image_url
        )
        # Return the actual status code from the processing result
        return jsonify(result), result.get("status_code", 200)

    except Exception as e:
        print(f"Error in /process-recipe endpoint: {e}") # Log the error server-side
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})


app.register_blueprint(recipe_bp)
if __name__ == "__main__":
    host=  os.getenv("NODE_ENV","dev")

    if host== "production":
        # debug off so wont see explanatory information in dockercompose or kubernetes
        app.run(debug=True, host='0.0.0.0', port=8082)
    elif host == 'dev':
        app.run(debug=True, host='0.0.0.0', port=5000)

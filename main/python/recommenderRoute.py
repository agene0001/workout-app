# recommenderRoute.py
import os
import sys
import logging
import signal
from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import MemoryEfficientRecommender
# from sparkRecommender import SparkRecommender
import mysql.connector
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z'
)
logger = logging.getLogger(__name__)

# Global variables
app = Flask(__name__)
CORS(app)
recipe_recommender = None
db_connection = None


def init_app():
    """Initialize application components"""
    global recipe_recommender, db_connection

    try:
        # Log startup information
        logger.info("Starting application...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Directory contents: {os.listdir('.')}")

        # Load environment variables
        load_dotenv()

        # Initialize database path (if needed)
        db_path = os.path.join(os.getcwd(), 'data', 'recipes.csv')
        logger.info(f"Using database path: {db_path}")

        # Initialize recommender
        logger.info("Initializing recommender...")
        is_docker = os.getenv('DOCKER') == 'true'
        is_docker_compose = os.getenv('DOCKERCOMPOSE') == 'true'
        logger.info(f"is docker = {is_docker}")
        logger.info(f"is docker compose = {is_docker_compose}")
        if is_docker:
            db_config = {
                'host': "mysql-db",
                'user': os.getenv('db_user'),
                'password': os.getenv('K8S_PASSWORD'),
                'database': os.getenv('db_name')
            }
        elif is_docker_compose:
            db_config = {
                'host': "mysql-db",
                'user': os.getenv('db_user'),
                'password': os.getenv('db_password'),
                'database': os.getenv('db_name')
            }
        else:
            db_config = {
                'host': os.getenv('db_host'),
                'user': os.getenv('db_user'),
                'password': os.getenv('db_password'),
                'database': os.getenv('db_name')
            }
        logger.info(f"Database configuration: {db_config}")

        recipe_recommender = MemoryEfficientRecommender(db_config, 'recipes')
        # results = recommender.find_ksimilar("target_item_name", 5)

        # recipe_recommender = SparkRecommender(db_config, 'recipes')

        recipe_recommender.preprocess()
        recipe_recommender.setup()
        # Prepare the data and generate the similarity matrix
        # if recipe_recommender.tfidf_matrix is None:
        #     recipe_recommender.setup('name', 'ingredients')
        #     logger.info("Recommender initialized successfully")

        # Database connection
        # if all(os.getenv(v) for v in ['db_host', 'db_user', 'db_password', 'db_name']):
        #     logger.info("Connecting to database...")
        #
        #     db_connection = mysql.connector.connect(
        #         host=os.getenv('db_host'),
        #         user=os.getenv('db_user'),
        #         password=os.getenv('db_password'),
        #         database=os.getenv('db_name')
        #     )
        #     logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.error("Stack trace:", exc_info=True)
        sys.exit(1)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}")
    if db_connection and db_connection.is_connected():
        logger.info("Closing database connection...")
        db_connection.close()
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Initialize the application
init_app()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'recommender_initialized': recipe_recommender is not None,
        'db_connected': db_connection is not None if db_connection else False
    })


NUM_MEALS = 5
MEAL_TYPES = ['breakfast', 'dinner', 'lunch', 'snack']
REQUIRED_MEALS = [1, 1, 1, 2]
TOLERANCE = 100
# myCursor = mydb.cursor()
# @app.route('/run_script', methods=['GET'])
# def run_script():
#     return jsonify({'result': 'Replace this with your Python script output'})

@app.route('/recommendations',methods=['GET'])
def get_recommendations():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({'error': 'No query parameter provided'}), 400

        k = int(request.args.get('k', 10))

        if recipe_recommender is None:
            return jsonify({'error': 'Recommender not initialized'}), 500

        recommendations = recipe_recommender.find_ksimilar(query, k, 'name')

        if recommendations.empty:
            return jsonify({'error': f'No recipe found matching "{query}"'}), 404

        return jsonify(recommendations[['name']].to_dict('records'))
    except Exception as e:
        logger.error(f"Recommendation error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/build_recipes', methods=['GET'])
def build_recipes():
    calories=int(request.args.get('calories'))
    meal_options=  make_random_meal_options()
    return generate_model(meal_options,calories)

def generate_model(meal_options,calories1):
    calories = np.array([option['calories'] for option in meal_options])

    # Element (i, j) == True iff meal i has meal type j, and False otherwise.
    meal_types = np.empty((len(meal_options), len(MEAL_TYPES)), dtype=bool)

    for i, option in enumerate(meal_options):
        for j, meal_type in enumerate(MEAL_TYPES):
            meal_types[i, j] = meal_type in option['types']

    model = cp_model.CpModel()

    # Decision variables, one for each meal and meal type: meal[i, j] is 1 iff
    # meal i is assigned to meal type j, and 0 otherwise.
    meal_vars = np.empty((len(meal_options), len(MEAL_TYPES)), dtype=object)

    for i in range(len(meal_options)):
        for j in range(len(MEAL_TYPES)):
            meal_vars[i, j] = model.NewBoolVar(f"meal[{i}, {j}]")

    # We want the overall caloric value of the meal plan to be within bounds.
    lb, ub = [calories1 - TOLERANCE, calories1 + TOLERANCE]
    model.AddLinearConstraint(calories @ meal_vars.sum(axis=1), lb, ub)

    for j, meal_type in enumerate(MEAL_TYPES):
        # Need the required amount of meals of each type.
        model.Add(meal_types[:, j] @ meal_vars[:, j] == REQUIRED_MEALS[j])

    for i in range(len(meal_options)):
        # Each meal can only be selected once across all meal types.
        model.Add(meal_vars[i, :].sum() <= 1)

    # Need NUM_MEALS meals in the meal plan
    model.Add(meal_vars.sum() == NUM_MEALS)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(f'total calories = {calories1}')
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Solving took {solver.WallTime():.2f} seconds")
        lis  = []
        for i in range(len(meal_options)):
            for j in range(len(MEAL_TYPES)):
                if solver.Value(meal_vars[i, j]) > 0:
                    option = meal_options[i]
                    cal = option['calories']
                    mt = MEAL_TYPES[j]
                    lis.append([option])
                    print(f"Selected meal {option['name']} {i} with {cal} calories for {mt}.")
        return lis
    else:
        print("No solution found.")

def make_random_meal_options():
    options = []
    query = "SELECT recipes.id,recipes.name,recipes.calories,categories.category_name,recipes.img_src,recipes.num_of_ratings,recipes.rating,recipes.ingredients,recipes.instructions FROM categories INNER JOIN recipe_categories ON categories.category_id=recipe_categories.category_id INNER JOIN recipes ON recipes.id=recipe_categories.recipe_id WHERE categories.category_name like %s"

    for i in MEAL_TYPES:
        myCursor.execute(query,(f'%{i}%',))
        items = myCursor.fetchall()
        for item in items:

            # for _ in range(200):
            calories = item[2]
            # print(calories)
            # print(item)
            num_types = np.random.randint(1, len(MEAL_TYPES))
            types = np.random.choice(MEAL_TYPES, num_types, replace=False)
            if calories != None:
                options.append(dict(calories=calories, types=i,name=item[1],img_src=item[4],num_of_ratings=item[5],ratings=item[6]))

    # List of dictionaries with keys 'calories' and 'types'
    return options

# Remove java route

if __name__ == '__main__':
    # Use production server
    from waitress import serve

    port = int(os.getenv('PORT', 8082))
    logger.info(f"Starting production server on port {port}")
    serve(app, host="0.0.0.0", port=port)

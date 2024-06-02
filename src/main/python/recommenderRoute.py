from flask import Flask, jsonify, request
from flask_cors import CORS
from recommender import Recommender
import mysql.connector
import numpy as np
from ortools.sat.python import cp_model



app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
dbPath = '../resources/static/recipes.csv'
recipeRecommender = Recommender(dbPath, 'recipes')
recipeRecommender.setup('name')
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="LexLuthern246!!??",
    database="automation"
)
myCursor = mydb.cursor()
@app.route('/run_script', methods=['GET'])
def run_script():
    return jsonify({'result': 'Replace this with your Python script output'})

@app.route('/recommendations',methods=['GET'])
def recommendation():
    query = request.args.get('query')
    print(query)
    return (jsonify(recipeRecommender.find_ksimilar(query,10,'name').transpose().to_dict()))

def make_random_meal_options():
    options = []
    myCursor.execute("")
    for _ in range(200):
        calories = np.random.randint(100, 1_000)
        num_types = np.random.randint(1, len(MEAL_TYPES))
        types = np.random.choice(MEAL_TYPES, num_types, replace=False)

        options.append(dict(calories=calories, types=types,name='belveta'))

    # List of dictionaries with keys 'calories' and 'types'
    return options
NUM_MEALS = 5
MEAL_TYPES = ['breakfast', 'dinner', 'lunch', 'snack']
REQUIRED_MEALS = [1, 1, 1, 2]
TARGET_CALORIES = 2_000
TOLERANCE = 50
# Remove java route
@app.route('/build_recipes',methods=['GET']):

if __name__ == '__main__':
    app.run(port=5000)

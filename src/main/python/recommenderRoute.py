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
NUM_MEALS = 5
MEAL_TYPES = ['breakfast', 'dinner', 'lunch', 'snack']
REQUIRED_MEALS = [1, 1, 1, 2]
TOLERANCE = 50
myCursor = mydb.cursor()
@app.route('/run_script', methods=['GET'])
def run_script():
    return jsonify({'result': 'Replace this with your Python script output'})

@app.route('/recommendations',methods=['GET'])
def recommendation():
    query = request.args.get('query')
    print(query)
    return (jsonify(recipeRecommender.find_ksimilar(query,10,'name').transpose().to_dict()))

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
    app.run(port=5000)

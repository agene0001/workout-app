# Assuming your parser code is in a file named `recipe_parser.py`
import pytest

from utils.NERModel.ingredient_parser import load_model
from xtractServer import extract_ingredients_ner# Import your function

# Define test cases: (input_string, expected_list_of_dicts)
ingredient_test_cases = [
    # Simple cases
    (["2 cups flour"], [{'name': 'flour', 'display_text': '2 cups flour', 'quantity': '2', 'unit': 'cups'}]),
    (["1 large egg"], [{'name': 'egg', 'display_text': '1 large egg', 'quantity': '1', 'unit': 'large'}]),
    (["salt"], [{'name': 'salt', 'display_text': 'salt', 'quantity': ''}]), # No quantity/unit

    # Fraction and mixed number quantities
    (["1/2 cup sugar"], [{'name': 'sugar', 'display_text': '1/2 cup sugar', 'quantity': '0.5', 'unit': 'cup'}]),
    (["1 1/2 tsp vanilla extract"], [{'name': 'vanilla extract', 'display_text': '1 1/2 tsp vanilla extract', 'quantity': '1.5', 'unit': 'tsp'}]),

    # Word quantities
    (["One large onion, chopped"], [{'name': 'onion', 'display_text': 'One large onion', 'quantity': '1', 'unit': 'large'}]),

    # More complex names and descriptors
    (["1/2 cup whole milk"], [{'name': 'whole milk', 'display_text': '1/2 cup whole milk', 'quantity': '0.5', 'unit': 'cup'}]),
    (["4 ounces cream cheese, at room temperature"], [{'name': 'cream cheese', 'display_text': '4 ounces cream cheese', 'quantity': '4', 'unit': 'ounces'}]),
    (["1 cup all-purpose flour"], [{'name': 'all-purpose flour', 'display_text': '1 cup all-purpose flour', 'quantity': '1', 'unit': 'cup'}]), # Check hyphen handling
    (["2 tablespoons unsalted butter, melted"], [{'name': 'unsalted butter', 'display_text': '2 tablespoons unsalted butter', 'quantity': '2', 'unit': 'tablespoons'}]),
    (["1 1/2 cups finely chopped pecans"] ,[{'name': 'chopped pecans', 'display_text': '1 1/2 cups finely chopped pecans', 'quantity': '1.5', 'unit': 'cups'}]),
    (["1 small bunch swiss chard or mustard greens stems removed leaves chopped"], [{'name': 'swiss chard', 'display_text': '1 small bunch swiss chard or mustard greens', 'quantity': '1', 'unit': 'small'}]),
    (["kosher salt and freshly ground pepper"], [{'name': 'kosher salt', 'display_text': 'kosher salt', 'quantity': ''},{'name': 'ground pepper', 'display_text': 'freshly ground pepper', 'quantity': ''}]),
    (["1 15-ounce can navy beans undrained"], [{'name': 'navy beans', 'display_text': '1 15-ounce can navy beans', 'quantity': '1', 'unit': 'can'}]),

    # Parentheses and commas
    (["Juice of 2 lemons (about 1/4 cup)"], [{'name': 'lemon juice', 'display_text': 'juice of 2 lemons (about 1/4 cup)', 'quantity': '0.25', 'unit': 'cup'}]), # Prefers standard unit
    (["1 can (15 ounces) black beans, rinsed and drained"], [{'name': 'black beans', 'display_text': '1 can (15 ounces) black beans', 'quantity': '1', 'unit': 'can'}]), # Ignores parenthesis content for name

    # Multiple ingredients (split by comma)
    (["1 cup flour"," 1/2 cup sugar"], [
        {'name': 'flour', 'display_text': '1 cup flour', 'quantity': '1', 'unit': 'cup'},
        {'name': 'sugar', 'display_text': '1/2 cup sugar', 'quantity': '0.5', 'unit': 'cup'}
    ]),
    (["1 large yellow squash about 8 ounces quartered lengthwise and sliced"],[{'name':'yellow squash about 8 ounces','display_text':'1 large yellow squash about 8 ounces','quantity':'1','unit':'large'}]),
    # Edge cases / Instructions to ignore
    (["Salt and pepper to taste"], [{'name': 'Salt and pepper', 'display_text': 'Salt and pepper', 'quantity': ''}]), # "to taste" is tricky, might need specific handling or accept this
    (["For the garnish: chopped parsley"], [{'name': 'chopped parsley', 'display_text': 'For the garnish: chopped parsley', 'quantity': ''}]), # "For the garnish:" should ideally be ignored or handled

    # Test case that previously failed
    (["2 tablespoons unsalted butter melted cooled plus more for brushing"],
     [{'name': 'unsalted butter', 'display_text': '2 tablespoons unsalted butter', 'quantity': '2',
       'unit': 'tablespoons'}]),

    # Seafood recipe ingredients
    (["20 clams, cleaned"], [{'name': 'clams', 'display_text': '20 clams', 'quantity': '20'}]),
    (["20 mussels, de-bearded and cleaned"],
     [{'name': 'mussels', 'display_text': '20 mussels', 'quantity': '20'}]),
    (["40 small rings of calamari, cleaned"],
     [{'name': 'calamari', 'display_text': '40 small rings of calamari', 'quantity': '40',
       'unit': 'small'}]),
    (["16 tiger shrimp, peeled and deveined"],
     [{'name': 'tiger shrimp', 'display_text': '16 tiger shrimp', 'quantity': '16'}]),
    (["1/4 cup extra-virgin olive oil"],
     [{'name': 'extra-virgin olive oil', 'display_text': '1/4 cup extra-virgin olive oil', 'quantity': '0.25',
       'unit': 'cup'}]),
    (["2 teaspoons chopped garlic"],
     [{'name': 'chopped garlic', 'display_text': '2 teaspoons chopped garlic', 'quantity': '2', 'unit': 'teaspoons'}]),
    (["1/4 cup italian parsley leaves, divided"],
     [{'name': 'italian parsley', 'display_text': '1/4 cup italian parsley', 'quantity': '0.25',
       'unit': 'cup'}]),
    (["1/8 teaspoon sea salt"],
     [{'name': 'sea salt', 'display_text': '1/8 teaspoon sea salt', 'quantity': '0.125', 'unit': 'teaspoon'}]),
    (["1/4 teaspoon crushed red pepper"],
     [{'name': 'red pepper', 'display_text': '1/4 teaspoon crushed red pepper', 'quantity': '0.25',
       'unit': 'teaspoon'}]),
    (["1 cup Pinot Grigio wine"],
     [{'name': 'Pinot Grigio wine', 'display_text': '1 cup Pinot Grigio wine', 'quantity': '1', 'unit': 'cup'}]),
    (["2 cups tomato sauce"],
     [{'name': 'tomato sauce', 'display_text': '2 cups tomato sauce', 'quantity': '2', 'unit': 'cups'}]),
    (["1 (1-pound) box dried spaghetti"],
     [{'name': 'box dried spaghetti', 'display_text': '1 (1-pound) box dried spaghetti', 'quantity': '1'}]),

    (["1 (200 g) large leek, cleaned, sliced ¼-inch-(.6 cm) thick"],
     [{'name': 'leek', 'display_text': '1 (200 g) large leek', 'quantity': '1','unit':'large'}]),
    (["6 cups (335 g) fresh kale, chopped, stems removed"],
     [{'name': 'fresh kale', 'display_text': '6 cups (335 g) fresh kale', 'quantity': '6','unit':'cups'}]),
    (["4 cups (960 ml) vegetable or chicken broth"],
     [{'name': 'chicken broth', 'display_text': '4 cups (960 ml) vegetable or chicken broth', 'quantity': '4','unit':'cups'}]),
    (["4 Japanese eggplants, cut in half lengthwise"],[{'name':'Japanese eggplants', 'display_text':'4 Japanese eggplants','quantity':"4"}]), # for simple eggplant parm
    (["4 Japanese eggplant, halved lengthwise"],[{'name':'Japanese eggplant', 'display_text':'4 Japanese eggplant','quantity':"4"}]), #grilled japanese eggplant
    (["4 Japanese eggplant, sliced lengthwise"],[{'name':'Japanese eggplant', 'display_text':'4 Japanese eggplant','quantity':"4"}]), # grilled japanese eggplant with citrus miso sauce
]
# broken recipes
# grilled chicken lettuce wraps with lemon-green olive tapenade
# kale and leek soup
@pytest.mark.parametrize("input_text, expected", ingredient_test_cases)
def test_ingredient_parsing(input_text, expected):
    """Tests the extract_ingredients function with various inputs."""
    # Need to handle potential spaCy model loading if it's slow,
    # but for en_core_web_sm it's usually fast enough to load per test run/module.
    # If using a larger model, consider pytest fixtures to load it once.
    result = extract_ingredients_ner(input_text)
    # Compare relevant fields, ignore minor display_text variations if needed
    # For simplicity, we compare the whole list directly here
    assert result == expected, f"Input: '{input_text}'"

# You can also add specific tests for the core name extraction
# from utils.ingredient_utils import extract_core_name_spacy
#
# core_name_test_cases = [
#     ("finely chopped pecans", "chopped pecans"),
#     ("whole milk", "whole milk"),
#     ("cream cheese at room temperature", "cream cheese"),
#     ("all - purpose flour", "all-purpose flour"), # Assuming cleanup handles space
#     ("unsalted butter melted cooled plus more for brushing", "unsalted butter"),
#     ("large eggs, beaten", "eggs"), # Example: assuming 'large' is treated as unit or removed here
#     ("salt and freshly ground black pepper", "salt and freshly ground black pepper"), # Keep multi-word
# ]
#
# @pytest.mark.parametrize("input_name, expected_core_name", core_name_test_cases)
# def test_core_name_extraction(input_name, expected_core_name):
#     assert extract_core_name_spacy(input_name).lower() == expected_core_name.lower()

if __name__=="__main__":
    # test_core_name_extraction()
    load_model()
    test_ingredient_parsing()
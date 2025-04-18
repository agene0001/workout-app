# Assuming your parser code is in a file named `recipe_parser.py`
import pytest
from xtractServer import extract_ingredients # Import your function

# Define test cases: (input_string, expected_list_of_dicts)
ingredient_test_cases = [
    # Simple cases
    ("2 cups flour", [{'name': 'flour', 'display_text': '2 cups flour', 'quantity': '2', 'unit': 'cups'}]),
    ("1 large egg", [{'name': 'egg', 'display_text': '1 large egg', 'quantity': '1', 'unit': 'large'}]),
    ("salt", [{'name': 'salt', 'display_text': 'salt', 'quantity': ''}]), # No quantity/unit

    # Fraction and mixed number quantities
    ("1/2 cup sugar", [{'name': 'sugar', 'display_text': '1/2 cup sugar', 'quantity': '0.5', 'unit': 'cup'}]),
    ("1 1/2 tsp vanilla extract", [{'name': 'vanilla extract', 'display_text': '1 1/2 tsp vanilla extract', 'quantity': '1.5', 'unit': 'tsp'}]),

    # Word quantities
    ("One large onion, chopped", [{'name': 'onion', 'display_text': 'one large onion', 'quantity': '1', 'unit': 'large'}]),

    # More complex names and descriptors
    ("1/2 cup whole milk", [{'name': 'whole milk', 'display_text': '1/2 cup whole milk', 'quantity': '0.5', 'unit': 'cup'}]),
    ("4 ounces cream cheese, at room temperature", [{'name': 'cream cheese', 'display_text': '4 ounces cream cheese', 'quantity': '4', 'unit': 'ounces'}]),
    ("1 cup all-purpose flour", [{'name': 'all-purpose flour', 'display_text': '1 cup all-purpose flour', 'quantity': '1', 'unit': 'cup'}]), # Check hyphen handling
    ("2 tablespoons unsalted butter, melted", [{'name': 'unsalted butter', 'display_text': '2 tablespoons unsalted butter', 'quantity': '2', 'unit': 'tablespoons'}]),
    ("1 1/2 cups finely chopped pecans", [{'name': 'chopped pecans', 'display_text': '1 1/2 cups finely chopped pecans', 'quantity': '1.5', 'unit': 'cups'}]),
    ("1 small bunch swiss chard or mustard greens stems removed leaves chopped", [{'name': 'chard', 'display_text': '1 small bunch swiss chard or mustard greens stems removed leaves chopped', 'quantity': '1', 'unit': 'bunch'}]),
    ("kosher salt and freshly ground pepper", [{'name': 'kosher salt', 'display_text': 'kosher salt', 'quantity': ''},{'name': 'ground pepper', 'display_text': 'freshly ground pepper', 'quantity': ''}]),
    ("1 15-ounce can navy beans undrained", [{'name': 'beans', 'display_text': '1 15-ounce can navy beans', 'quantity': '1', 'unit': 'can'}]),

    # Parentheses and commas
    ("Juice of 2 lemons (about 1/4 cup)", [{'name': 'lemon juice', 'display_text': 'juice of 2 lemons (about 1/4 cup)', 'quantity': '0.25', 'unit': 'cup'}]), # Prefers standard unit
    ("1 can (15 ounces) black beans, rinsed and drained", [{'name': 'black beans', 'display_text': '1 can (15 ounces) black beans', 'quantity': '1', 'unit': 'can'}]), # Ignores parenthesis content for name

    # Multiple ingredients (split by comma)
    ("1 cup flour, 1/2 cup sugar", [
        {'name': 'flour', 'display_text': '1 cup flour', 'quantity': '1', 'unit': 'cup'},
        {'name': 'sugar', 'display_text': '1/2 cup sugar', 'quantity': '0.5', 'unit': 'cup'}
    ]),

    # Edge cases / Instructions to ignore
    ("Salt and pepper to taste", [{'name': 'salt and pepper', 'display_text': 'salt and pepper to taste', 'quantity': ''}]), # "to taste" is tricky, might need specific handling or accept this
    ("For the garnish: chopped parsley", [{'name': 'chopped parsley', 'display_text': 'for the garnish: chopped parsley', 'quantity': ''}]), # "For the garnish:" should ideally be ignored or handled

    # Test case that previously failed
    ("2 tablespoons unsalted butter melted cooled plus more for brushing", [{'name': 'unsalted butter', 'display_text': '2 tablespoons unsalted butter melted cooled plus more for brushing', 'quantity': '2', 'unit': 'tablespoons'}])
]

@pytest.mark.parametrize("input_text, expected", ingredient_test_cases)
def test_ingredient_parsing(input_text, expected):
    """Tests the extract_ingredients function with various inputs."""
    # Need to handle potential spaCy model loading if it's slow,
    # but for en_core_web_sm it's usually fast enough to load per test run/module.
    # If using a larger model, consider pytest fixtures to load it once.
    result = extract_ingredients(input_text)
    # Compare relevant fields, ignore minor display_text variations if needed
    # For simplicity, we compare the whole list directly here
    assert result == expected, f"Input: '{input_text}'"

# You can also add specific tests for the core name extraction
from ingredient_utils import extract_core_name_spacy

core_name_test_cases = [
    ("finely chopped pecans", "chopped pecans"),
    ("whole milk", "whole milk"),
    ("cream cheese at room temperature", "cream cheese"),
    ("all - purpose flour", "all-purpose flour"), # Assuming cleanup handles space
    ("unsalted butter melted cooled plus more for brushing", "unsalted butter"),
    ("large eggs, beaten", "eggs"), # Example: assuming 'large' is treated as unit or removed here
    ("salt and freshly ground black pepper", "salt and freshly ground black pepper"), # Keep multi-word
]

@pytest.mark.parametrize("input_name, expected_core_name", core_name_test_cases)
def test_core_name_extraction(input_name, expected_core_name):
    assert extract_core_name_spacy(input_name).lower() == expected_core_name.lower()

if __name__=="__main__":
    test_core_name_extraction()
    test_ingredient_parsing()
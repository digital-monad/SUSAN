import pandas as pd
from ast import literal_eval

# Test data:

test_ingredients = ["milk", "vanilla ice cream", "frozen apple juice concentrate", "apple"]

# Path to database (change this to fname later). Use RAW_recipes for now.

path = "/Users/Elijah/Sus-Recipes/food-com-recipes-and-user-interactions/RAW_recipes.csv"
path2 = "/Users/Elijah/Sus-Recipes/food-com-recipes-and-user-interactions/PP_recipes.csv"


# Some helper functions before the rank function - these will not be used in the final version.
def read(path):
    file = pd.read_csv(path)
    return file


# Searches the database to return a list of recipes sorted by missing ingredient.
def search(path):
    recs = []
    file = read(path)
    for index, rec in file.iterrows():
        ings = literal_eval(rec["ingredients"])
        diff = set(ings) - set(test_ingredients)
        if len(diff) <= 2:
            recs.append((len(diff), rec))
    recs.sort(key=lambda x: x[0])
    return recs


print(search(path), len(search(path)))

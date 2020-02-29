import pandas as pd
from ast import literal_eval


# Test data:

test_ingredients = ["milk", "vanilla ice cream", "frozen apple juice concentrate", "apple"]

# Path to database. Use RAW_recipes for now.

path = "/Users/Elijah/Sus-Recipes/food-com-recipes-and-user-interactions/RAW_recipes.csv"
path2 = "/Users/Elijah/Sus-Recipes/food-com-recipes-and-user-interactions/PP_recipes.csv"


# Some helper functions before the rank function - these will not be used in the final version.
def read(path):
    file = pd.read_csv(path)
    return file


# Searches the database to return a list of recipes sorted by missing ingredient.
def search(path):
    print("Searching the database...")
    df = read(path)
    recs = df.get(["name", "ingredients", "nutrition", "description"])
    ings = recs.get("ingredients")

    result = []

    for i in range(len(ings)):
        ing = literal_eval(ings.iloc[i])
        diff = set(ing) - set(test_ingredients)
        if len(diff) <= 2:
            result.append((len(diff), recs.iloc[i]))
    result.sort(key=lambda x: x[0])
    return result


print(search(path))

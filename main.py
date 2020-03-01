import numpy as np
import pandas as pd
import json
from ast import literal_eval


# Test data
test_ingredients = ["milk", "vanilla ice cream", "frozen apple juice concentrate", "apple"]


# Path to database. Use RAW_recipes for now
path = "/Users/Elijah/Sus-Recipes/SR/database.csv"


# Some helper functions before the rank function - these will not be used in the final version
def read(path):
    file = pd.read_csv(path)
    return file


# Searches the database to return a list of recipes sorted by missing ingredient
def search(path):
    print("Searching the database...")
    df = read(path)
    recs = df.get(["name", "ingredients", "nutrition", "description", "id"])
    ings = recs.get("ingredients")
    result = []
    for i in range(len(ings)):
        ing = ings.iloc[i]
        ing = literal_eval(ing)
        diff = set(ing) - set(test_ingredients)
        if len(diff) <= 2:
            result.append((len(diff), recs.iloc[i]))
    result.sort(key=lambda x: x[0])
    return result


# Scores a single recipe by expiring ingredients
def score_by_exp(rec_ings, ingr_list):
    s = 0
    exp_list = [0, 8, 30, 2]
    weighted_list = list(map(lambda x: 1 / (1 + x), exp_list))
    for i in range(len(rec_ings)):
        if rec_ings[i] in ingr_list:
            s += weighted_list[ingr_list.index(rec_ings[i])]
    return s


# Scores a single recipe by nutritional value of recipe
def score_by_nutr(rec_nutr):
    nutrition_weights = np.array([0, -1, -3, 1, 2, -3, 1])
    return np.sum(np.multiply(nutrition_weights, rec_nutr))


# Score the recipes by expiry date
def score(ingr_list, recs):
    scores = []
    for rec in recs:
        rec_ings = literal_eval(rec[1].get("ingredients"))
        rec_nutr = np.array(json.loads(rec[1].get("nutrition")))
        rec_id = rec[1].get("id")
        score = score_by_exp(rec_ings, ingr_list) + score_by_nutr(rec_nutr)
        print("Score: {}, ID: {}".format(score, rec_id))
        scores.append(score)
    return scores


score(test_ingredients, search(path))

import pandas as pd
from ast import literal_eval


# Test data:

test_ingredients = ["milk", "vanilla ice cream", "frozen apple juice concentrate", "apple"]
exp_list = [0,8,30,2]
n1 = 1
weighted_list = map (lambda x : n1/(1+x), exp_list)


# Path to database. Use RAW_recipes for now.

path = "./RAW_recipes.csv"
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




def score_ingr(ingr_list,reps): # Score the recipes by expiry date
    scores = []
    for i in range(len(reps)):
        scores.append(scoreByIng(literal_eval(search(path)[i][1]['ingredients']),test_ingredients))
    return scores

def scoreByIng(rec_ings,ingr_list): # Scores a single recipe by expiring ingredients
    s = 0
    w = list(weighted_list)
    for i in range(len(rec_ings)):
        print(rec_ings[i])
        if rec_ings[i] in ingr_list:
            print('is in ingredients')
            s += w[ingr_list.index(rec_ings[i])]
    return s

print(scoreByIng(literal_eval(search(path)[12][1]['ingredients']),test_ingredients))
#print(score_ingr(test_ingredients,search(path)))
#print(scoreByIng(literal_eval(search(path)[12][1]['ingredients']),test_ingredients))
#print(scoreByIng(literal_eval(search(path)[12][1]['ingredients']),test_ingredients))
import json
import numpy as np
import pandas as pd
import speaker as sp
import sys
from ast import literal_eval


# Test data
test_ingredients = ["banana", "orange juice", "butter", "milk"]


# Path to database. Use RAW_recipes for now
path = "/Users/Elijah/Sus-Recipes/SR/database.csv"


# Some helper functions before the rank function - these will not be used in the final version
def read(path):
    file = pd.read_csv(path)
    return file


# Searches the database to return a list of recipes sorted by missing ingredient
def search(path):
    print("\nWelcome! I'm SUSAN. I'm here to help you reduce your food waste. The ingredients you've given me are:\n")
    for ing in test_ingredients:
        print(ing.capitalize())
    sp.synth("Welcome! I'm SUSAN. I'm here to help you reduce your food waste. The ingredients you've given me are:", "utt")
    for i in test_ingredients:
        sp.synth(i, "ingredient")
    print("\nSearching the database, please wait a moment...")
    sp.synth("Searching the database. Please wait a moment.", "utt")
    df = read(path)
    recs = df.get(["name", "ingredients", "nutrition", "description", "id"])
    ings = recs.get("ingredients")
    print("Evaluating the results...")
    sp.synth("Evaluating the results.", "utt")
    result = []
    missing_1 = []
    missing_2 = []
    for i in range(len(ings)):
        ing = ings.iloc[i]
        ing = literal_eval(ing)
        diff = set(ing) - set(test_ingredients)
        if len(diff) <= 2:
            result.append((len(diff), recs.iloc[i]))
        if len(diff) == 1:
            missing_1.append(recs.iloc[i])
        if len(diff) == 2:
            missing_2.append(recs.iloc[i])
    result.sort(key=lambda x: x[0], reverse=True)
    return result, missing_1, missing_2


# Scores a single recipe by expiring ingredients
def score_by_exp(rec_ings, ingr_list):
    s = 0
    exp_list = [0, 2, 8, 10]
    weighted_list = list(map(lambda x: 5 / (1 + x), exp_list))
    for i in range(len(rec_ings)):
        if rec_ings[i] in ingr_list:
            s += weighted_list[ingr_list.index(rec_ings[i])]
    return s


# Scores a single recipe by nutritional value of recipe
def score_by_nutr(rec_nutr):
    normalised = np.array([0, -1/99, -3/99, 1/99, 2/99, -3/99, 1/72])
    nutrition_weight = normalised*np.sum(normalised)
    return np.sum(np.multiply(nutrition_weight, rec_nutr))


# Score the recipes by expiry date
def score(ingr_list, recs):
    scores = []
    for rec in recs:
        rec_ings = literal_eval(rec[1].get("ingredients"))
        rec_nutr = np.array(json.loads(rec[1].get("nutrition")))
        score = score_by_exp(rec_ings, ingr_list) + score_by_nutr(rec_nutr)
        scores.append((score, rec))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


# For better output in the terminal
def prettify(final, n):

    nutr_units = ["cal", "g", "g", "mg", "g", "g", "g"]

    for i in range(n):
        name = final[i][1]["name"]
        ings = final[i][1]["ingredients"]
        nutrs = final[i][1]["nutrition"]
        id = final[i][1]["id"]
        url = "https://www.food.com/search/"+to_string(id)
        ings = literal_eval(ings)
        nutrs = json.loads(nutrs)
        print("\n--- Recipe {} ---".format(i + 1))
        print("\nName: "+name.title())
        print("\nIngredients:\n ")
        for ing in ings:
            if ing not in test_ingredients:
                print(ing.capitalize())
        print("\nNutrition:\n ")
        for n in range(len(nutrs)):
            print(str(nutrs[n])+nutr_units[n])

        print("\nURL: "+url)

    print("\nDon't hesitate to click on the URL of the recipe that looks best!")
    sp.synth("Here are the recipes for the 20 dishes that make the most out of your ingredients. "
             "Don't hesitate to click on the URL of the recipe that looks best!", "utt")


def to_string(x):
    return str(list(np.reshape(np.asarray(x), (1, np.size(x)))[0]))[1:-1]


def prettify_single(mn, n, nutr_units):
    missing_ings = []
    for i in range(n):
        m = mn[i]
        name = m.get("name")
        ings = m.get("ingredients")
        ings = literal_eval(ings)
        nutrs = m.get("nutrition")
        nutrs = json.loads(nutrs)
        id = m.get("id")
        url = "https://www.food.com/search/"+to_string(id)
        print("\n--- Recipe {} ---".format(i + 1))
        print("\nName: " + name.title())
        print("\nIngredient(s) needed:\n ")
        for ing in ings:
            if ing not in test_ingredients:
                missing_ings.append(ing)
                print(ing.capitalize())
        print("\nNutrition:\n ")
        for n in range(len(nutrs)):
            print(str(nutrs[n]) + nutr_units[n])
        print("\nURL: "+url)
    return missing_ings


# Writes to text file for TTS output
def write(all_m_ings):
    f = open("./shopping_list.txt", "w")
    f.write("The ingredients you need are:\n\n")
    for m in all_m_ings:
        f.write(m.capitalize()+"\n")


def prettify_missing(m1, m2, n):

    nutr_units = ["cal", "g", "g", "mg", "g", "g", "g"]

    print("\nAs a bonus, you're only missing a couple more ingredients for these dishes:")
    print("\nDishes where you're only missing one ingredient:")

    m_ings_1 = prettify_single(m1, n, nutr_units)

    print("\nDishes where you're missing two ingredients:")

    m_ings_2 = prettify_single(m2, n, nutr_units)

    all_m_ings = set(m_ings_1+m_ings_2)
    write(all_m_ings)


def get_recipes(path):
    r, m1, m2 = search(path)
    ys = ["yes", "yeah", "yup", "y", " yes", " yeah", " yup", " y"]
    nos = ["no", "nah", "nope", "n", " no", " nah", " nope", "n"]
    scores = score(test_ingredients, r)
    final = [s[1] for s in scores]
    prettify(final, 20)
    sp.synth("Would you like to see some extra recipes?", "utt")
    t = True
    while t:
        inp = input("Would you like to see some extra recipes?")
        if inp in ys:
            sp.synth("No problem:", "utt")
            prettify_missing(m1, m2, 5)
            sp.synth("I've also compiled a shopping list for you in case you want to make any of these dishes. "
                     "Would you like me to read it?", "utt")
            t = True
            while t:
                print()
                inp2 = input("I've compiled a shopping list for you in case you want to make any of these dishes. "
                             "Would you like me to read it?")

                if inp2 in ys:
                    print("Alright here goes...")
                    sp.synth("Alright here goes...", "utt")
                    sp.read_shopping("./shopping_list.txt")
                    print("See you soon!")
                    sys.exit(0)

                elif inp2 in nos:
                    print("\nOk. See you soon!\n")
                    sp.synth("Ok. See you soon!", "utt")
                    sys.exit(0)

                else:
                    print("Sorry I didn't quite catch that.")
                    sp.synth("Sorry I didn't quite catch that.", "utt")

        elif inp in nos:
            print("\nOk. See you soon!\n")
            sp.synth("Ok. See you soon!", "utt")
            sys.exit(0)

        else:
            print("Sorry I didn't quite catch that.")
            sp.synth("Sorry I didn't quite catch that.", "utt")


def main():
    get_recipes(path)


if __name__ == "__main__":
    main()

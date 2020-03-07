import json
import sys
import re
import numpy as np
import pandas as pd
import speaker as sp
from ast import literal_eval


# Test data
user_ingredients = ["rice", "chicken", "soy sauce", "garlic"]
# user_ingredients = ["banana", "orange juice", "butter", "milk"]

# Expiry weights (the units are days to expiry)
exp_list = [0, 2, 8, 1]

# Path to database. Use RAW_recipes for now
path = "./database.csv"


# Some helper functions before the rank function - these will not be used in the final version
def read(path):
    file = pd.read_csv(path)
    return file


# Searches the database to return a list of recipes sorted by missing ingredient
def search(path):
    print("\nWelcome! I'm SUSAN. I'm here to help you reduce your food waste. \n")
    print("Your ingredients:\n")
    for ing in user_ingredients:
        print(ing.capitalize())
    sp.synth("Welcome! I'm SUSAN. I'm here to help you reduce your food waste.", "utt")
    print("\nSearching the database, please wait a moment...")
    sp.synth("Searching the database. Please wait a moment.", "utt")
    df = read(path)
    recs = df.get(["name", "ingredients", "nutrition", "description", "id"])
    ings = recs.get("ingredients")
    names = recs.get("name")
    print("Evaluating the results...")
    sp.synth("Evaluating the results.", "utt")
    unique_names = []
    result = []
    for i in range(len(ings)):
        ing = ings.iloc[i]
        ing = literal_eval(ing)
        rec_name = names.iloc[i]
        diff = set(ing) - set(user_ingredients)
        if len(diff) <= 2 and rec_name not in unique_names:
            unique_names.append(rec_name)
            result.append((len(diff), recs.iloc[i]))
    result.sort(key=lambda x: x[0], reverse=True)
    return result


# Scores a single recipe by expiring ingredients
def score_by_exp(rec_ings, ingr_list, exp_list):
    s = 0
    weighted_list = list(map(lambda x: 1 / (1 + x), exp_list))
    for i in range(len(rec_ings)):
        if rec_ings[i] in ingr_list:
            s += weighted_list[ingr_list.index(rec_ings[i])]
    return s


# Scores a single recipe by nutritional value of recipe
def score_by_nutr(rec_nutr):
    normalised = np.array([0, -1/99, -3/99, 1/99, 2/99, -3/99, 1/72])
    nutrition_weight = normalised*np.sum(normalised)
    return np.sum(np.multiply(nutrition_weight, rec_nutr))


# Score the recipes by expiry date and nutritional value
def score(ingr_list, recs):
    scores = []
    for rec in recs:
        rec_ings = literal_eval(rec[1].get("ingredients"))
        rec_nutr = np.array(json.loads(rec[1].get("nutrition")))
        score = score_by_exp(rec_ings, ingr_list, exp_list) + score_by_nutr(rec_nutr)
        scores.append((score, rec))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


# Helper functions to better print descriptions
def find_lows(string):
    single_space = string
    for i in range(len(re.findall("\.  \w", string))):
        single_space = single_space.replace(".  ", ". ")
    stops = re.findall("\. \w", single_space)
    lows = []
    for stop in stops:
        match = re.search("[a-z]", stop)
        lows.append(match.group())

    return single_space, lows


def to_cap(string):
    single_space, lows = find_lows(string)
    result = single_space
    for low in lows:
        result = result.replace(". {}".format(low), ". {}".format(low.upper()))
    return result


# For nicer output to the terminal
def prettify(final, scores, m, n):

    nutr_names = ["Calories", "Total fat", "Sugars", "Sodium", "Protein", "Saturated fat", "Carbohydrates"]

    for i in range(m, n):
        name = final[i][1]["name"]
        ings = final[i][1]["ingredients"]
        nutrs = final[i][1]["nutrition"]
        rec_id = final[i][1]["id"]
        desc = final[i][1]["description"]
        score = scores[i][0]
        url = "https://www.food.com/search/"+to_string(rec_id)
        ings = literal_eval(ings)
        nutrs = json.loads(nutrs)
        print("\n--- Recipe {} ---".format(i + 1))
        print("\nName: "+name.title())
        print("\nDescription: \n")
        desc = str(desc)
        desc = desc.capitalize()
        if len(desc.split()) >= 30:
            print(desc.split(".")[0]+".")
        else:
            print(to_cap(desc))
        print("\nIngredients:\n ")
        for ing in ings:
            print(ing.capitalize())
        print("\nNutrition:\n ")
        print("Calories: "+str(nutrs[0])+"cal")
        for n in range(1, len(nutrs)):
            print(nutr_names[n]+": "+str(nutrs[n])+"% of daily intake")
        print("\nNttur score: " + str(round(score, 2)))
        print("\nURL: "+url)


# Helper function for displaying URL
def to_string(x):
    return str(list(np.reshape(np.asarray(x), (1, np.size(x)))[0]))[1:-1]


# Compiles shopping list and writes result to file(s)
def compile_shopping_list(desired_recs):
    f = open("./shopping_list.txt", "w")
    g = open("./read_shopping_list.txt", "w")
    f.write("The ingredients you need are:\n")
    g.write("The ingredients you need are:\n")
    nums = [rec[0] for rec in desired_recs]
    ings = [literal_eval(rec[1].get("ingredients")) for rec in desired_recs]
    diffs = [list(set(ing)-set(user_ingredients)) for ing in ings]
    unique = []
    for i in range(len(diffs)):
        diff = diffs[i]
        num = nums[i]
        f.write("\n--- Recipe {} ---\n\n".format(num))
        for d in diff:
            f.write(d.capitalize()+"\n")
            if d not in unique:
                unique.append(d)
                g.write(d.capitalize()+"\n")


# Main function
def get_recipes(path):
    r = search(path)
    ys = ["yes", "yeah", "yup", "y", " yes", " yeah", " yup", " y"]
    nos = ["no", "nah", "nope", "n", " no", " nah", " nope", "n"]
    scores = score(user_ingredients, r)
    final = [s[1] for s in scores]
    prettify(final, scores, 0, 20)
    print("\nDon't hesitate to click on the URL of the recipe that looks best!")
    sp.synth("Here are the recipes for the 20 dishes that make the most out of the ingredients you gave me. "
             "Don't hesitate to click on the URL of the recipe that looks best!", "utt")
    sp.synth("Would you like to see more recipes?", "utt")
    m = 20
    t = True
    while t:
        desired_recs = []
        t2 = True
        while t2:
            inp = input("\nWould you like to see more recipes? (y/n) " )
            if inp in ys:
                if m < len(scores):
                    prettify(final, scores, m, m + 10)
                    m += 10
                else:
                    print("No more recipes for this combination of ingredients :(")
                    sp.synth("I don't have any more recipes for these ingredients. Sorry!")
            elif inp in nos:
                sp.synth("Enter the number of a recipe you'd like to make.", "utt")
                t3 = True
                while t3:
                    num = int(input("Enter the number of a recipe you'd like to make (0 to quit): "))
                    if num == 0:
                        print("\nOk. See you soon!")
                        sp.synth("Ok. see you soon!", "utt")
                        sys.exit(0)
                    if num-1 < m:
                        rec = final[num - 1][1]
                        desired_recs.append((num, rec))
                        t4 = True
                        while t4:
                            inp = input("Want to make another recipe? (y/n) ")
                            if inp in ys:
                                break
                            elif inp in nos:
                                compile_shopping_list(desired_recs)
                                sp.synth("I've compiled a shopping list for the dishes you want to make. Would you "
                                         "like me to read it?", "utt")
                                inp = input("I've compiled a shopping list for the dishes you want to make. Would you "
                                            "like me to read it? (y/n) ")
                                if inp in ys:
                                    sp.read_shopping("./read_shopping_list.txt")
                                    print("\nSee you soon!")
                                    sys.exit(0)
                                elif inp in nos:
                                    print("\nOk. See you soon!")
                                    sp.synth("Ok. See you soon!", "utt")
                                    sys.exit(0)
                                else:
                                    print("Sorry, I didn't quite catch that.")
                                    sp.synth("Sorry, I didn't quite catch that.", "utt")
                            else:
                                print("Sorry, I didn't quite catch that.")
                    else:
                        print("Sorry, that number is out of bounds. Try again.")
                        sp.synth("Sorry, that number is out of bounds. Try again.", "utt")
            else:
                print("Sorry I didn't quite catch that.")
                sp.synth("Sorry I didn't quite catch that.", "utt")


def main():
    get_recipes(path)


if __name__ == "__main__":
    main()

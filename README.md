# Sus-Recipes
**Input** : ingredients you have, dietary requirements (?). 
**Output** : recipes given the ingredients and potentially two sustainable shopping lists: one for missing items and one for all ingredients (for next time you want to make the dish). 

## Front end:

- Two pages.
- First page - inputs (ingredients, exp dates, requirements).
- Second page - recipes and URLs, brief description of dish, etc.

## Main steps to implement:

From input:

1. Search database for recipes with those ingredients.
2. Rank the recipes by expiry date of ingredients.
3. Take top *n* of this list and rank recipes by nutritional value.
3. Rank top *n* recipes by least number of ingredients to buy and uses most of the ingredients you have. 
4. Recommend alternative recipes that include the missing ingredients.

## ML feature (?):

- Stores the tags of the recipes that they select.
- Based on that data, builds a model of the user's tastes. Borrow from HTB V?

## Shopping list feature (?):

- Generates a list of missing ingredients (once a recipe is selected).
- Source sustainably. 
- Read out shopping list. 

## Output:

A list of recipes, synthetic speech output of shopping lists.  

## Extensions:

- meal of the day (classification?). 


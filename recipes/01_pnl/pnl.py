#!/usr/bin/env python

# Import the Panacea Recipe Maker 
import sys
sys.path.append('D:\\Projects\\python\\')
from panacea_recipe_maker.recipe import *

############################
# Ingredient specifications:
############################

pale = Malt("Pale Ale Malt", price = 13)
dextros = Malt("Dextrose", price = 27)

jarrylo = Hop("Jarrylo", alpha = 13.4, price = 59)
mosaic = Hop("Mosaic", alpha = 10.4, price = 89)
citra = Hop("Citra", alpha = 13.5, price = 89)

us_05 = Yeast("US-05", price = 35)

############################
# Recipe specifications:
############################

recipe = Recipe("Pears & Lemons", 19, 1.087, 65)
# Adjusting OG for late addition of dextrose
recipe = Recipe("Pears & Lemons", 19, 1.076, 65)

# Grain bill
recipe.addIngredient(time = "Mash", ingredient = pale, amount = 6)
recipe.addIngredient(time = "@10 min", ingredient = dextros, amount = 0.6)

# Hop schedule
recipe.addIngredient(time = 60, ingredient = jarrylo, amount = 11)
recipe.addIngredient(time = 60, ingredient = citra, amount = 8)
recipe.addIngredient(time = 60, ingredient = mosaic, amount = 14)

recipe.addIngredient(time = 20, ingredient = jarrylo, amount = 24)
recipe.addIngredient(time = 20, ingredient = citra, amount = 17)
recipe.addIngredient(time = 20, ingredient = mosaic, amount = 20)

recipe.addIngredient(time = 0, ingredient = jarrylo, amount = 25)
recipe.addIngredient(time = 0, ingredient = citra, amount = 35)
recipe.addIngredient(time = 0, ingredient = mosaic, amount = 26)

#Dry hopping
recipe.addIngredient(time = "Dry hop 5 days", ingredient = jarrylo, amount = 40)
recipe.addIngredient(time = "Dry hop 5 days", ingredient = citra, amount = 40)
recipe.addIngredient(time = "Dry hop 5 days", ingredient = mosaic, amount = 40)

# Fermentation
recipe.addIngredient(time = "After cooling wort", ingredient = us_05, amount = 1.4)

# Generate and print recipe
recipe.printRecipe()

sys.stdout = open('recipe.txt', 'w')
recipe.printRecipe()
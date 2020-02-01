#!/usr/bin/env python

# Import the Panacea Recipe Maker 
import sys
sys.path.append('..\\..\\')
from pathlib import Path
from panacea_recipe_maker.recipe import *

############################
# Ingredient specifications:
############################

pilsner = Malt("Pilsner Malt", price = 15)
pale_ale_malt = Malt("Pale Ale Malt", price = 15)
biscuit_malt = Malt("Biscuit Malt", price = 32)
caramunich_iii = Malt("Caramünich III (53-61 LB)", price = 18)
chocolate_malt = Malt("Chocolate Malt", price = 29)

columbus = Hop("Columbus", alpha = 13.9, price = 69)

us_05 = Yeast("US-05", price = 29)

############################
# Recipe specifications:
############################

recipe = Recipe("Oh, Mama!", 19, 1.054, 68)

# Grain bill
recipe.addIngredient(time = "Mash", ingredient = pilsner, amount = 3.127)
recipe.addIngredient(time = "Mash", ingredient = pale_ale_malt, amount = 0.11)
recipe.addIngredient(time = "Mash", ingredient = biscuit_malt, amount = 0.631)
recipe.addIngredient(time = "Mash", ingredient = caramunich_iii, amount = 0.234)
recipe.addIngredient(time = "Mash", ingredient = chocolate_malt, amount = 0.18)

# Hop schedule
recipe.addIngredient(time = 60, ingredient = columbus, ibu = 15.6)

recipe.addIngredient(time = 30, ingredient = columbus, ibu = 10.8)

recipe.addIngredient(time = 15, ingredient = columbus, ibu = 5.44)

# Fermentation
recipe.addIngredient(time = "After cooling wort", ingredient = us_05, amount = 1)

# Generate and print recipe
recipe.printRecipe()

sys.stdout = open(Path(__file__).stem+'.md', 'w')
recipe.printRecipe()

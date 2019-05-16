#!/usr/bin/env python

# Import the Panacea Recipe Maker 
import sys
sys.path.append('D:\\Projects\\python\\')
from panacea_recipe_maker.recipe import *

############################
# Ingredient specifications:
############################

# Import the Panacea inventory
sys.path.append('D:\\Projects\\Bryggning\\')
import inventory

pale = Malt("Pale Ale Malt", price = 13)
wheat = Malt("Wheat Malt", price = 16)
peated = Malt("Peated Malt", price = 30)
caram3 = Malt("Caramünich III Malt", price = 18)
choc = Malt("Chocolate Malt", price = 29)
black = Malt("Black Patent Malt", price = 29)
roast = Malt("Roasted Barley", price = 0)

columbus = Hop("Columbus", alpha = 14.6, price = 69)

b4 = Yeast("B4 English Ale", price = 29)

############################
# Recipe specifications:
############################

recipe = Recipe("Schweiss, Bier und Stahl - Die Arbeiterporter", 19, 1.065, 67)

# Grain bill
recipe.addIngredient(time = "Mash", ingredient = pale, amount = 3.5)
recipe.addIngredient(time = "Mash", ingredient = wheat, amount = 0.5)
recipe.addIngredient(time = "Mash", ingredient = peated, amount = 0.35)
recipe.addIngredient(time = "Mash", ingredient = caram3, amount = 0.2)
recipe.addIngredient(time = "Mash", ingredient = choc, amount = 0.15)
recipe.addIngredient(time = "Mash", ingredient = black, amount = 0.1)
recipe.addIngredient(time = "Mash", ingredient = roast, amount = 0.1)

# Hop schedule
recipe.addIngredient(time = 60, ingredient = columbus, amount = 28)

# Fermentation
recipe.addIngredient(time = "After cooling wort", ingredient = b4, amount = 1)

# Generate and print recipe
recipe.printRecipe()

sys.stdout = open('recipe.txt', 'w')
recipe.printRecipe()
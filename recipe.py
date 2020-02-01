#!/usr/bin/env python

from panacea_recipe_maker.ingredients import Malt, Hop, Yeast, Ingredient
from panacea_recipe_maker.printer import Printer

# TODOS:
# - Calculations for gravity from fermentables?
# - Fermentation print
# - Other ingredients
# - Dynamic recipe? % in malts, IBU in hops, yeast packs based on OG? Major upvote

class Recipe:
    'Common base class for all recipes'
    def __init__(self, name, batchSize, originalGravity, mashTemp = 65, mashTime = 60, mashOutTemp = 75, mashOutTime = 10):
        self.name = name
        self.originalGravity = originalGravity
        # Batch size in liters
        self.batchSize = batchSize
        self.mashTemp = mashTemp
        self.mashTime = mashTime
        self.mashOutTemp = mashOutTemp
        self.mashOutTime = mashOutTime
        self.ingredients = []
        
    def addIngredient(self, ingredient, amount, time):
        self.ingredients.append(Ingredient(ingredient, amount, time))
        
    def getTotalMashGrains(self, comp):
        totalAmount = 0.0
        for ingredient in self.ingredients:
            if type(ingredient.type) is comp and (ingredient.time) is "Mash":
               totalAmount += ingredient.amount
        return totalAmount
        
    def getTotalGrains(self, comp):
        totalAmount = 0.0
        for ingredient in self.ingredients:
            if type(ingredient.type) is comp:
               totalAmount += ingredient.amount
        return totalAmount
    
    # For Grainfather that is....
    def getMashVolume(self):
        grainCoeff = 2.7
        deadspace = 3.5
        return (self.getTotalMashGrains(Malt) * grainCoeff) + deadspace
        
    def getSpargeVolume(self):
        absorbCoeff = 0.8
        return self.getPreBoilVolume() - self.getMashVolume() + (self.getTotalMashGrains(Malt) * absorbCoeff)
     
    def getPreBoilVolume(self):
        loss = 5 # 3 @ boil, 2 @ transfer
        return self.batchSize + loss
        
    def getPostBoilVolume(self):
        trub = 2 # 3 @ boil, 2 @ transfer
        return self.batchSize + trub
        
    def getPreBoilGravity(self):
        gPoints = self.originalGravity - 1
        return 1 + gPoints * (self.getPostBoilVolume()/self.getPreBoilVolume())
        
    def printRecipe(self):
        Printer(self).printRecipe()

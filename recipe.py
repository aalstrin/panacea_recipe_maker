#!/usr/bin/env python

from panacea_recipe_maker.ingredients import Malt, Hop, Yeast, Ingredient
from panacea_recipe_maker.printer import Printer

import copy

# TODOS:
# - Calculations for gravity from fermentables?
# - Fermentation print
# - Other ingredients
# - Dynamic recipe? % in malts, yeast packs based on OG? Major upvote

class HopStage:
    def __init__(self, time, recipe):
        self.time = time
        self.ibu = 0
        self.hops = []
        self.preBoilGravity = recipe.getPreBoilGravity()
        self.getPostBoilVolume = recipe.getPostBoilVolume()
    
    def addHop(self, ingredient):
        hop = ingredient.type
        self.ibu = self.ibu + hop.ibu
        self.hops.append(ingredient)

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
        self.hopStages = []
        
    def addIngredient(self, ingredient, time, amount = 0, ibu = 0):        
        # Type specific operations
        if(type(ingredient) is Hop):
            newHop = copy.deepcopy(ingredient)
        
            if ibu != 0:
                amount = newHop.getAmount(ibu, time, self.getPreBoilGravity(), self.getPostBoilVolume())
            
            newHop.getIBU(amount*Hop.amountUnit, time, self.getPreBoilGravity(), self.getPostBoilVolume())
                
            # Is it a stage already existing?
            currentHopStage = None
            for hopStage in self.hopStages:
                if (time == hopStage.time):
                    currentHopStage = hopStage
                    break
                    
            if(currentHopStage == None):            
                # Not found, create it
                currentHopStage = HopStage(time, self)
                self.hopStages.append(currentHopStage)
                
            newIngredient = Ingredient(type = newHop, amount = amount, time = time)
            currentHopStage.addHop(newIngredient)
        else:
            # Only handle hops for now
            newIngredient = Ingredient(type = ingredient, amount = amount, time = time)
            
        self.ingredients.append(newIngredient)
        
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
    
    def getTotalIBUs(self):
        totalIbu = 0 
        for hopStage in self.hopStages:
            totalIbu += hopStage.ibu
        return totalIbu            
        
    def printRecipe(self):
        Printer(self).printRecipe()

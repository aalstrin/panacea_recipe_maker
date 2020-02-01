#!/usr/bin/env python
from panacea_recipe_maker.ingredients import Malt, Hop, Yeast, Ingredient
from decimal import *

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
    
    def printName(self):
        print("# Recipe for: " + self.name)
        print()
        print("Goal batch size: " + str(self.batchSize) + " l")
        print("Goal OG: " + str(self.originalGravity))
        print()
        
    def printGrainBillAndMash(self):
        print("## Grainbill and mashing")
        print()
        getcontext().prec = 2
        for ingredient in self.ingredients:
            if type(ingredient.type) is Malt:
                nameStr = ingredient.type.name               
                qStr = str(100*Decimal(ingredient.amount) / Decimal(self.getTotalGrains(Malt))) + "% \t"
                amountStr = str(ingredient.amount / Malt.amountUnit) + " " + Malt.amountUnitText + " \t"
                timeStr = str(ingredient.time)
                print('{:28}'.format(nameStr) + qStr + amountStr + timeStr)
        print("Total mash grain weight: " + str(self.getTotalMashGrains(Malt)) + " " + Malt.amountUnitText)
        print("Total grain weight: " + str(self.getTotalGrains(Malt)) + " " + Malt.amountUnitText)
        print()
        print("Mash volume: " + str(self.getMashVolume()) + " l")
        print("Mash temperature: " + str(self.mashTemp) + "°C")
        print("Mash time: " + str(self.mashTime) + " min")
        print("Mash out at " + str(self.mashOutTemp) + "°C for " + str(self.mashOutTime) + " min." )
        print("Sparge volume: " + str(self.getSpargeVolume()) + " l")
        print()

    def printHopSchedule(self):
        print("## Hop schedule and boil")
        print()
        print("Pre-boil volume: " + str(self.getPreBoilVolume()) + " l")
        getcontext().prec = 4
        print("Pre-boil gravity: " + str(Decimal(self.getPreBoilGravity()) / Decimal(1)))
        print("Post-boil volume: " + str(self.getPostBoilVolume()) + " l\n")
        
        getcontext().prec = 3
        totalIbu = 0;
        currentTime = -1
        stageIBU = 0
        dryHopStr = "Post-boil ingredients:\n"
        for ingredient in self.ingredients:
            if type(ingredient.type) is Hop:
                nameStr = ingredient.type.name
                alphaStr = str(ingredient.type.alpha) + " %"
                amountStr = str(ingredient.amount / ingredient.type.amountUnit) + " " + ingredient.type.amountUnitText + "\t"
                
                if isinstance(ingredient.time, int): 
                    if ingredient.time != currentTime and currentTime != -1:
                        stageIBU = totalIbu - stageIBU
                        print("Total IBUs for stage: " + str(Decimal(stageIBU) / Decimal(1)) + "\n")
                    currentTime = ingredient.time                        
                    timeStr = "@" + str(ingredient.time) + " min\t"                                       
                    ibu = ingredient.type.getIBU(ingredient.amount / ingredient.type.amountUnit, ingredient.time, self.getPreBoilGravity(), self.getPostBoilVolume())
                    totalIbu += ibu
                    ibuStr = str(Decimal(ibu) / Decimal(1)) + " IBUs"
                    print(timeStr + '{:13}'.format(nameStr) + '{:10}'.format(alphaStr) + amountStr + ibuStr)
                else:
                    dryHopStr += '{:20}'.format(str(ingredient.time)) + '{:13}'.format(nameStr) + '{:10}'.format(alphaStr) + amountStr + "\n"
                    
        print("Total IBUs: " + str(Decimal(totalIbu) / Decimal(1)))
        print()
        print(dryHopStr)
        
    def printCost(self):
        print("## Other")
        print()
        print("Cost of the ingredients in recipe:")
        cost = 0.0
        for ingredient in self.ingredients:
            cost += ingredient.amount * ingredient.type.price
        print(str(cost) + "kr")
        print()
    
    def printRecipe(self):
        self.printName()
        self.printGrainBillAndMash()
        self.printHopSchedule()
        self.printCost()
            

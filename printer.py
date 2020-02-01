#!/usr/bin/env python

from panacea_recipe_maker.recipe import *
from decimal import *

class Printer:
    def __init__(self, recipe):
        self.recipe = recipe
        
    def printName(self):
        print("# Recipe for: " + self.recipe.name)
        print()
        print("Goal batch size: " + str(self.recipe.batchSize) + " l")
        print("Goal OG: " + str(self.recipe.originalGravity))
        print()
        
    def printGrainBillAndMash(self):
        print("## Grainbill and mashing")
        print()
        getcontext().prec = 2
        for ingredient in self.recipe.ingredients:
            if type(ingredient.type) is Malt:
                nameStr = ingredient.type.name               
                qStr = str(100*Decimal(ingredient.amount) / Decimal(self.recipe.getTotalGrains(Malt))) + "% \t"
                amountStr = str(ingredient.amount / Malt.amountUnit) + " " + Malt.amountUnitText + " \t"
                timeStr = str(ingredient.time)
                print('{:28}'.format(nameStr) + qStr + amountStr + timeStr)
        print("Total mash grain weight: " + str(self.recipe.getTotalMashGrains(Malt)) + " " + Malt.amountUnitText)
        print("Total grain weight: " + str(self.recipe.getTotalGrains(Malt)) + " " + Malt.amountUnitText)
        print()
        print("Mash volume: " + str(self.recipe.getMashVolume()) + " l")
        print("Mash temperature: " + str(self.recipe.mashTemp) + "°C")
        print("Mash time: " + str(self.recipe.mashTime) + " min")
        print("Mash out at " + str(self.recipe.mashOutTemp) + "°C for " + str(self.recipe.mashOutTime) + " min." )
        print("Sparge volume: " + str(self.recipe.getSpargeVolume()) + " l")
        print()

    def printHopSchedule(self):
        print("## Hop schedule and boil")
        print()
        print("Pre-boil volume: " + str(self.recipe.getPreBoilVolume()) + " l")
        getcontext().prec = 4
        print("Pre-boil gravity: " + str(Decimal(self.recipe.getPreBoilGravity()) / Decimal(1)))
        print("Post-boil volume: " + str(self.recipe.getPostBoilVolume()) + " l\n")
        
        getcontext().prec = 3
        totalIbu = 0;
        currentTime = -1
        stageIBU = 0
        dryHopStr = "Post-boil ingredients:\n"
        for ingredient in self.recipe.ingredients:
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
                    ibu = ingredient.type.getIBU(ingredient.amount / ingredient.type.amountUnit, ingredient.time, self.recipe.getPreBoilGravity(), self.recipe.getPostBoilVolume())
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
        for ingredient in self.recipe.ingredients:
            cost += ingredient.amount * ingredient.type.price
        print(str(cost) + "kr")
        print()
    
    def printRecipe(self):
        self.printName()
        self.printGrainBillAndMash()
        self.printHopSchedule()
        self.printCost()
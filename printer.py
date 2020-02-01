#!/usr/bin/env python

from panacea_recipe_maker.recipe import *
from decimal import *

class Printer:
    def __init__(self, recipe):
        self.recipe = recipe
        
    def getFloatString(self, float, prec):
        getcontext().prec = prec
        return str(Decimal(float)/Decimal(1))
        
    def printName(self):
        print("# Recipe for: " + self.recipe.name)
        print()
        print("Goal batch size: " + str(self.recipe.batchSize) + " l")
        print("Goal OG: " + str(self.recipe.originalGravity))
        print()
        
    def printGrainBillAndMash(self):
        print("## Grainbill and mashing")
        print()
        for ingredient in self.recipe.ingredients:
            if type(ingredient.type) is Malt:
                nameStr = ingredient.type.name               
                qStr = self.getFloatString(100*ingredient.amount / self.recipe.getTotalGrains(Malt), 2) + "% \t"
                amountStr = self.getFloatString((ingredient.amount / Malt.amountUnit), 3) + " " + Malt.amountUnitText + " \t"
                timeStr = str(ingredient.time)
                print('{:28}'.format(nameStr) + qStr + amountStr + timeStr)
        print("Total mash grain weight: " + self.getFloatString(self.recipe.getTotalMashGrains(Malt),3) + " " + Malt.amountUnitText)
        print("Total grain weight: " + self.getFloatString(self.recipe.getTotalGrains(Malt), 3) + " " + Malt.amountUnitText)
        print()
        print("Mash volume: " + self.getFloatString(self.recipe.getMashVolume(), 4) + " l")
        print("Mash temperature: " + str(self.recipe.mashTemp) + "°C")
        print("Mash time: " + str(self.recipe.mashTime) + " min")
        print("Mash out at " + str(self.recipe.mashOutTemp) + "°C for " + str(self.recipe.mashOutTime) + " min." )
        print("Sparge volume: " + self.getFloatString(self.recipe.getSpargeVolume(), 4) + " l")
        print()

    def printHopSchedule(self):
        print("## Hop schedule and boil")
        print()
        print("Pre-boil volume: " + str(self.recipe.getPreBoilVolume()) + " l")
        print("Pre-boil gravity: " + self.getFloatString(self.recipe.getPreBoilGravity(), 4))
        print("Post-boil volume: " + str(self.recipe.getPostBoilVolume()) + " l\n")
        
        totalIbu = 0;
        currentTime = -1
        stageIBU = 0
        dryHopStr = "Post-boil ingredients:\n"
        for hopStage in self.recipe.hopStages:
            boil = True
            for ingredient in hopStage.hops:
                hop = ingredient.type
                nameStr = hop.name
                alphaStr = str(hop.alpha) + " %"
                amountStr = self.getFloatString(ingredient.amount / Hop.amountUnit, 3) + " " + Hop.amountUnitText + "\t"
            
                if type(hopStage.time) is str:
                    dryHopStr += '{:20}'.format(str(hopStage.time)) + '{:13}'.format(nameStr) + '{:10}'.format(alphaStr) + amountStr + "\n"
                    boil = False
                else:
                    timeStr = "@" + str(hopStage.time) + " min\t"                    
                    ibuStr = self.getFloatString(hop.ibu, 3) + " IBUs"
                    print(timeStr + '{:13}'.format(nameStr) + '{:10}'.format(alphaStr) + amountStr + ibuStr)
            if boil:       
                print("Total IBUs for stage: " + self.getFloatString(hopStage.ibu, 3) + "\n")
            
        print("Total IBUs: " + self.getFloatString(self.recipe.getTotalIBUs(), 3))
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
#!/usr/bin/env python
from math import *

class Malt:
    'Common base class for all malts'
    # Specify what amount (in kg) is specified as the price unit.
    priceUnit = 1.0
    # Specify what amount (in kg) is specified as the amount unit.
    amountUnit = 1.0
    amountUnitText = "kg"
 
    def __init__(self, name, price):
        self.name = name
        self.price = price / Malt.priceUnit

class Hop:
    'Common base class for all hops, formulas from http://realbeer.com/hops/research.html'
    # Specify what amount (in kg) is specified as the price unit.
    priceUnit = 0.1
    # Specify what amount (in kg) is specified as the amount unit.
    amountUnit = 0.001
    amountUnitText = "g"
 
    def __init__(self, name, alpha, price):
        self.name = name
        self.alpha = alpha
        self.price = price / Hop.priceUnit
        self.ibu = 0
    
    def getIBU(self, amount, time, boilGravity, finalVolume):
        # mg/l of alpha acids
        if type(time) is str:
            return 0
        cAlpha = (self.alpha * (amount/self.amountUnit) * 10) / finalVolume        
        self.ibu = cAlpha * Hop.getHopUtilization(boilGravity, time)
        return self.ibu
    
    def getHopUtilization(boilGravity, time):
        gravityFactor = 1.65 * 0.000125 ** (boilGravity - 1.0)
        timeFactor = (1 - exp(-0.04 * time)) /4.15
        return gravityFactor * timeFactor
        
    def getAmount(self, ibu, time, boilGravity, finalVolume):
        q = Hop.getHopUtilization(boilGravity, time) * self.alpha * 10
        return (ibu*finalVolume)/q
        
class Yeast:
    'Common base class for all yeasts'
    # Specify what amount (in kg) is specified as the price unit.
    priceUnit = 0.0115
    # Specify what amount (in kg) is specified as the amount unit.
    amountUnit = 0.0115
    amountUnitText = "pkg"
 
    def __init__(self, name, price):
        self.name = name
        self.price = price / Yeast.priceUnit

class Ingredient:
    def __init__(self, type, time, amount):
        self.type = type
        self.amount = amount * type.amountUnit
        self.time = time
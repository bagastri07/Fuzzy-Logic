#Import libraries
import pandas as pd
import numpy as np

#import excel dataset
import_data = pd.read_excel('restoran.xlsx')
data = import_data.to_numpy().copy()

#Membership function that use trapezoidal
def memb_service_high(x, a = 65, b = 80):
    if x <= a:
        return 0
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b:
        return 1

def memb_service_med(x, a = 40, b = 55, c = 70, d = 75):
    if x <= a or x >= d:
        return 0
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b and x <= c:
        return 1
    if x > c and x <= d:
        return -1 * (x - d) / (d - c)

def memb_service_low(x, a = 20, b = 50):
    if x <= a:
        return 1
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b:
        return 0

def memb_food_high(x, a= 5, b = 9):
    if x <= a:
        return 0
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b:
        return 1

def memb_food_med(x, a = 3, b = 5, c = 6, d = 8):
    if x <= a or x >= d:
        return 0
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b and x <= c:
        return 1
    if x > c and x <= d:
        return -1 * (x - d) / (d - c)

def memb_food_low(x, a = 3, b = 5.5):
    if x <= a:
        return 1
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b:
        return 0

#Fuzzification
def fuzzy_service(service_value):
    service_set_value = {
        'high': memb_service_high(service_value),
        'med' : memb_service_med(service_value),
        'low' : memb_service_low(service_value)
    }
    return service_set_value

def fuzzy_food(food_value):
    service_set_value = {
        'high': memb_food_high(food_value),
        'med' : memb_food_med(food_value),
        'low' : memb_food_low(food_value)
    }
    return service_set_value

print(fuzzy_food(5))

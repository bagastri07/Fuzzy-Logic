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

#Inference
def inference_rule(service_value_set, food_value_set):
    inference_value_set = {
        'suggested': [],
        'considered': [],
        'unrecommended': []
    }
    #Using clipping technique, conjunction rule will get the minumum value
    inference_value_set['suggested'].append(min(service_value_set['high'], food_value_set['high']))
    inference_value_set['suggested'].append(min(service_value_set['high'], food_value_set['med']))
    inference_value_set['considered'].append(min(service_value_set['high'], food_value_set['low']))

    inference_value_set['suggested'].append(min(service_value_set['med'], food_value_set['high']))
    inference_value_set['considered'].append(min(service_value_set['med'], food_value_set['med']))
    inference_value_set['unrecommended'].append(min(service_value_set['med'], food_value_set['low']))

    inference_value_set['considered'].append(min(service_value_set['low'], food_value_set['high']))
    inference_value_set['unrecommended'].append(min(service_value_set['low'], food_value_set['med']))
    inference_value_set['unrecommended'].append(min(service_value_set['low'], food_value_set['low']))

    #Yse disjunction rule, get the max value for each fuzzy value
    inference_value_set['suggested'] = max(inference_value_set['suggested'])
    inference_value_set['considered'] = max(inference_value_set['considered'])
    inference_value_set['unrecommended'] = max(inference_value_set['unrecommended'])

    return inference_value_set

def defuzzification(inference_value_set):
    CONSTANT_SUGGESTED = 100
    CONSTANT_CONSIDERED = 70
    CONTANT_UNRECOMMENDED = 40

    a = ((inference_value_set['unrecommended'] * CONTANT_UNRECOMMENDED) + (inference_value_set['considered'] * CONSTANT_CONSIDERED) + (inference_value_set['suggested'] * CONSTANT_SUGGESTED))
    b = inference_value_set['unrecommended'] + inference_value_set['considered'] + inference_value_set['suggested']

    return a / b

a = fuzzy_food(6)
b = fuzzy_service(58)
print(inference_rule(a, b))

print(defuzzification(inference_rule(a, b)))

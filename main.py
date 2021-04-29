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

#membership func mamdani
def memb_suggested(x, max, a = 65, b = 80):
    if x <= a:
        return 0
    if x > a and x < b:
        temp = (x - a) / (b - a)
        if temp < max:
            return (x - a) / (b - a)
        else:
            return max
    if x >= b:
        return max

def memb_considered(x, max, a = 40, b = 55, c = 70, d = 75):
    if x <= a or x >= d:
        return 0
    if x > a and x < b:
        return (x - a) / (b - a)
    if x >= b and x <= c:
        return max
    if x > c and x <= d:
        temp = -1 * (x - d) / (d - c)
        if temp < max:
            return temp
        else:
            return max

def memb_unrecommended(x, max, a = 20, b = 50):
    if x <= a:
        return max
    if x > a and x < b:
        temp = (x - a) / (b - a)
        if temp < max:
            return temp
        else:
            return max
    if x >= b:
        return 0

def defuzzification(inference_value_set):
    random_set = [10, 25, 40, 45, 60, 75, 90, 95]

    defuz_set = {
        'suggested': [],
        'considered': [],
        'unrecommended': []
    }
    for i in range(len(random_set)):
        defuz_set['suggested'].append(memb_suggested(random_set[i], inference_value_set['suggested']))
        defuz_set['considered'].append(memb_considered(random_set[i], inference_value_set['considered']))
        defuz_set['unrecommended'].append(memb_unrecommended(random_set[i], inference_value_set['unrecommended']))
    
    final_defuz_set = []
    for i in range(len(random_set)):
        final_defuz_set.append(max(defuz_set['unrecommended'][i], defuz_set['considered'][i], defuz_set['suggested'][i]))
    
    upp = 0
    for i in range(len(random_set)):
        upp = (random_set[i]*final_defuz_set[i]) + upp
    bott = 0
    for i in range(len(random_set)):
        bott = final_defuz_set[i] + bott

    return upp / bott
   

def main():
    #import excel dataset
    import_data = pd.read_excel('restoran.xlsx')
    data = import_data.to_numpy().copy()

    # # print(data[i, 1])
    # inference_set = []
    # for i in range(len(data)):
    #     inf_temp = inference_rule(fuzzy_service(data[i, 1]), fuzzy_food(data[i, 2]))
    #     defuzzy_temp = defuzzification(inf_temp)
    #     inference_set.append([defuzzy_temp, i])
    #     # print(defuzzy_temp)
    # inference_set.sort(reverse=True)
    # print(inference_set)


a = inference_rule(fuzzy_service(93), fuzzy_food(4))
print(defuzzification(a))



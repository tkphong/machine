import numpy as np
import requests
import json
import random

def gen_dummy_temp(lower_bound=29, upper_bound=35, k=192):
    return np.random.choice(upper_bound - lower_bound, k) + np.array([lower_bound] * k)

def get_random_temp():
    lower_bound = 29
    upper_bound = 35
    k = 195
    return np.random.randint(lower_bound, upper_bound+1, k)
    

def get_temp():
    result = requests.get(
        "http://localhost:8080/api/getRecords"
    )
    temp_list = [record["temperature"] for record in result.json()]
    return temp_list


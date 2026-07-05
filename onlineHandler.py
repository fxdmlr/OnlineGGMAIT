import requests
import random
import json

url = 'https://guardts.ir/api/pastes'

def generate_random_sequence(length):
    string = ""
    arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'] 
    for i in range(length):
        string += arr[random.randint(0, len(arr) - 1)]
    
    return string

def create_new_file(text, addr):
    r = requests.post(url, data={
        "content" : text,
        "customSlug": addr,
        "expiresIn":"1"
    })
    
    return r

def read_addr(addr):
    r = requests.get(url + "/" + addr)#.text
    resp = json.loads(r.text)
    return resp["content"]


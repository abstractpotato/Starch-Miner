import random
import requests
import json
import time
import datetime
from hashlib import sha256

host = "http://starch.one/api"

def get_minerID():
    print("Enter Miner ID:")
    minerID = input().upper()

    # Clean input
    if len(minerID) != 8:
        print(f"Error: {minerID} is an invalid Miner ID!")
        print("Please try again")
        return ""

    # Confirm the Miner ID is active
    r = requests.post(f"{host}/status", json={"minerID": minerID})
    result = json.loads(r.text)
    
    if result["amount"] < 0:
        print(f"Error: {minerID} not found!")
        print("Make sure this Miner ID is activated before mining.")
        return ""
    
    return minerID


def get_color():
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    return '#' + hex_number[2:]


def solve(last_hash, minerID, max_value):
    running = True

    while running:
        color = get_color()
        string = f'{last_hash} {minerID} {color}'
        new_hash = sha256(string.encode()).hexdigest()
        value = int(new_hash, 16)
        
        if value < max_value:
            x = datetime.datetime.now()
            dtime = x.strftime("%m/%d/%Y-%H:%M:%S")
            
            print(dtime, new_hash)
            running = False
            return {"newHash": new_hash, "color": color, "minerID": minerID}


def mine(minerID):
    x = datetime.datetime.now()
    dtime = x.strftime("%m/%d/%Y-%H:%M:%S")

    r = requests.get(f"{host}/mine")
    result = json.loads(r.text)
    last_hash = result["last_hash"]
    max_value = result["max"]
    
    temp_hash = last_hash
    s = solve(last_hash, minerID, max_value)
    
    count = 0
    
    while True:
        count += 1
        
        x = datetime.datetime.now()
        dtime = x.strftime("%m/%d/%Y-%H:%M:%S")
        
        r = requests.get(f"{host}/mine")
        result = json.loads(r.text)
        
        last_hash = result["last_hash"]
        max_value = result["max"]
        
        if temp_hash != last_hash:
            temp_hash = last_hash
            s = solve(last_hash, minerID, max_value)
    
        r = requests.post(f"{host}/solved", json=s)
        result = json.loads(r.text)

        if result["success"] == "True":
            print(dtime, s, "Block Mined!", count)
        
        time.sleep(.1)


print("Starch Industries Miner - Beta 1.0")
print("Created By: Abstract Potato")
print()

minerID = get_minerID()

if minerID != "":
    while True:
        mine(minerID)

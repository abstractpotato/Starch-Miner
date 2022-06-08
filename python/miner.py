import os
import random
import requests
import json
import time
import datetime
from hashlib import sha256

host = "https://starch.one/api"


def get_minerID():
    if os.name =="nt":
        os.system("cls")
  
    # for linux / Mac OS
    else:
        os.system("clear")
        
    print("--------------------------------------------")
    print("Starch Industries Miner - Beta 1.2")
    print("Created By: Abstract Potato")
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
            running = False
            return {"newHash": new_hash, "color": color, "minerID": minerID}


def mine(minerID):
    start_time = datetime.datetime.now()
    block_count = 0
    
    while True:
        result = json.loads(requests.get(f"{host}/mine").text)
        s = solve(result["last_hash"], minerID, max_value=result["max"])
        result = json.loads(requests.post(f"{host}/solved", json=s).text)
        
        if os.name =="nt":
            os.system("cls")
      
        # for linux / Mac OS
        else:
            os.system("clear")
            
        if result["success"] == "True":
            block_count += 1

        current_time = datetime.datetime.now()
        running_time = str(current_time - start_time)[:-7]
        
        print("--------------------------------------------")
        print("Starch Industries Miner - Beta 1.2")
        print("Created By: Abstract Potato")
        print(f"Miner ID: {minerID}")
        print("--------------------------------------------")
        print("Start Time          | Runtime | New Blocks")
        print(f"{start_time.strftime('%m/%d/%Y-%H:%M:%S')} | {running_time} | {block_count}")
        print("--------------------------------------------")

        time.sleep(.001)


minerID = get_minerID()

if minerID != "":
    while True:
        mine(minerID)

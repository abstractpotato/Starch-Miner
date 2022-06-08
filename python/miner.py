import os
import random
import requests
import json
import datetime
from hashlib import sha256

host = "https://starch.one/api"
version = "beta v1.2.2"


def clear_console():
    if os.name == "nt":
        os.system("cls")

    # for linux / Mac OS
    else:
        os.system("clear")


def fix_line(text):
    while len(text) < 40:
        text += " "
    text += "│"
    print(text)


def print_head(is_closed=True):
    print("┌───────────────────────────────────────┐")
    fix_line(f"│ Starch Industries Miner - {version}")
    fix_line("│ Created By: @abstractpotato")
    if is_closed:
        print("└───────────────────────────────────────┘")


def print_status(minerID, start_time, running_time, block_count, newHash):
    print_head(False)
    print("├────────────┬──────────────────────────┤")
    fix_line(f"│ Miner ID   │ {minerID}")
    print("├────────────┼──────────────────────────┤")
    fix_line(f"│ Running    │ {newHash[0:10]}...{newHash[-10:]}")
    print("├────────────┼──────────────────────────┤")
    fix_line(f"│ Start Time | {start_time.strftime('%m/%d/%Y-%H:%M:%S')}")
    print("├────────────┼──────────────────────────┤")
    fix_line(f"| Runtime    | {running_time}")
    print("├────────────┼──────────────────────────┤")
    fix_line(f"| New Blocks | {block_count}")
    print("└────────────┴──────────────────────────┘")


def get_minerID():
    clear_console()
    print_head()
    print("> Enter Miner ID:")
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


def attempt(minerID):
    result = json.loads(requests.get(f"{host}/mine").text)
    s = solve(result["last_hash"], minerID, max_value=result["max"])
    result = json.loads(requests.post(f"{host}/solved", json=s).text)
    return result, s


def mine(minerID):
    start_time = datetime.datetime.now()
    block_count = 0

    while True:
        result = attempt(minerID)
        clear_console()

        if result[0]["success"] == "True":
            block_count += 1

        current_time = datetime.datetime.now()
        running_time = str(current_time - start_time)[:-7]

        print_status(minerID, start_time, running_time,
                     block_count, result[1]["newHash"])


minerID = get_minerID()

if minerID != "":
    while True:
        mine(minerID)

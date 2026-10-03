import json

with open("inventory/devices.json") as file:
    inventory = json.load(file)

device = inventory["devices"][0]

print(device)
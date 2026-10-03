import json
from netmiko import ConnectHandler

with open("inventory/devices.json") as file:
    inventory = json.load(file)

device = inventory["devices"][0]

connection = {
    "device_type": device["device_type"],
    "host": device["host"],
    "username": device["username"],
    "password": "cisco",
    "secret": "cisco"
}

net_connect = ConnectHandler(**connection)

print("Connected to R1")

net_connect.disconnect()
print("Connection closed")
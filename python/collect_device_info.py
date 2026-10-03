import json
import re
from pathlib import Path

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
net_connect.enable()

version_output = net_connect.send_command("show version")

interface_data = net_connect.send_command(
    "show ip interface brief",
    use_textfsm=True
)

hostname = net_connect.find_prompt().replace("#", "").strip()

version_match = re.search(
    r"Version ([0-9.]+)",
    version_output
)

ios_version = (
    version_match.group(1)
    if version_match
    else "Unknown"
)

uptime_match = re.search(
    rf"{re.escape(hostname)} uptime is (.+)",
    version_output
)

uptime = (
    uptime_match.group(1)
    if uptime_match
    else "Unknown"
)

interfaces = []

for interface in interface_data:
    interfaces.append({
        "interface": interface.get("interface"),
        "ip_address": interface.get("ip_address"),
        "status": interface.get("status"),
        "protocol": interface.get("proto")
    })

net_connect.disconnect()

report = {
    "hostname": hostname,
    "ios_version": ios_version,
    "uptime": uptime,
    "interfaces": interfaces
}

output_dir = Path("api")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / f"{hostname.lower()}-device-info.json"

with open(output_file, "w") as file:
    json.dump(report, file, indent=4)

print("\n=== DEVICE INFORMATION ===")
print(json.dumps(report, indent=4))

print("\n=== REPORT SAVED ===")
print(output_file)
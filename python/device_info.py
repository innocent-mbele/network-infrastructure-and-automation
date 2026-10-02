from netmiko import ConnectHandler
import json
import re
from pathlib import Path


# Cisco device connection details
device = {
    "device_type": "cisco_ios",
    "host": "10.10.20.171",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


# Connect to the Cisco device
connection = ConnectHandler(**device)
connection.enable()


# Collect device information
version_output = connection.send_command("show version")

interface_data = connection.send_command(
    "show ip interface brief",
    use_textfsm=True
)


# Extract hostname
hostname = connection.find_prompt().replace("#", "").strip()


# Extract IOS version
version_match = re.search(
    r"Version ([0-9.]+)",
    version_output
)

ios_version = (
    version_match.group(1)
    if version_match
    else "Unknown"
)


# Extract uptime
uptime_match = re.search(
    r"R1 uptime is (.+)",
    version_output
)

uptime = (
    uptime_match.group(1)
    if uptime_match
    else "Unknown"
)


# Build structured interface information
interfaces = []

for interface in interface_data:
    interfaces.append({
        "interface": interface.get("interface"),
        "ip_address": interface.get("ip_address"),
        "status": interface.get("status"),
        "protocol": interface.get("proto")
    })


# Close the SSH connection
connection.disconnect()


# Build final report
report = {
    "hostname": hostname,
    "ios_version": ios_version,
    "uptime": uptime,
    "interfaces": interfaces
}


# Create output directory
output_dir = Path("api")
output_dir.mkdir(exist_ok=True)


# Save JSON report
output_file = output_dir / "r1-device-info.json"

with open(output_file, "w") as file:
    json.dump(report, file, indent=4)


# Display result
print("\n=== DEVICE INFORMATION ===")
print(json.dumps(report, indent=4))

print("\n=== REPORT SAVED ===")
print(output_file)
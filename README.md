# System Update Monitor - MQTT Integration

## Overview
System Update Monitor is a Python-based project that checks for available system updates using `apt` and publishes this information via MQTT. This enables seamless integration with automation platforms like Home Assistant for monitoring and managing system updates.

## Features
- Executes `sudo apt update` and `sudo apt list --upgradable` to gather data on upgradable packages.
- Publishes the total number of upgradable packages and their details to an MQTT broker.
- Configures an MQTT sensor in Home Assistant for automatic discovery.
- Sends detailed package information as JSON attributes.

## Requirements
- Python 3.x
- `paho-mqtt` library (install with `pip install paho-mqtt`)
- Permissions to run `sudo apt` commands

## Installation
1. Clone this repository or copy the script file to your local system.
2. Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```
 
Install the required Python package:
  ```bash
pip install paho-mqtt
```
Configuration
Edit the script to match your MQTT broker details:

  ```python

MQTT_SERVER = "192.168.1.1"  # Replace with your MQTT broker IP
MQTT_PORT = 1883  # Adjust the port if necessary
DISCOVERY_PREFIX = "homeassistant"  # Change if using a different prefix
  ```

## Usage
Run the script using Python:

  ```bash
sudo python3 system_update_monitor.py
```
Note: The script requires sudo to run apt commands.

## How It Works

The script uses subprocess to run sudo apt update and sudo apt list --upgradable.
Parses the output and collects details of upgradable packages.
Formats the data as JSON and sends it via MQTT.
Configures a Home Assistant sensor to display the number of upgradable packages and package details.
MQTT Configuration for Home Assistant
The script publishes data to topics under homeassistant/sensor/system_update. The sensor configuration message includes:


name: Sensor name (e.g., "System Update")
state_topic: Topic where the number of upgradable packages is published
json_attributes_topic: Topic for detailed package data
Example MQTT Message
```json
{
  "total_upgradable": 3,
  "packages": [
    {
      "package": "package1",
      "current_version": "1.0",
      "new_version": "1.1"
    },
    {
      "package": "package2",
      "current_version": "2.3",
      "new_version": "2.4"
    }
  ]
}
```

## Crontab 

Sample: Hourly update for homeassistant sample 

```bash
0 * * * * sudo python3 /home/username/apt_update.py >> /dev/null 2>&1 
```


## Enhancements
Add error handling for subprocess commands.
Schedule the script as a cron job for regular checks.
Secure script execution to avoid unnecessary sudo usage.

## License
This project is licensed under the MIT License.

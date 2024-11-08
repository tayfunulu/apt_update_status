import subprocess
import json
import paho.mqtt.client as mqtt
import time

# MQTT Setup
MQTT_SERVER = "192.168.1.100"  # MQTT broker IP adress 
MQTT_PORT = 1883  # MQTT broker port
DISCOVERY_PREFIX = "homeassistant"  # Auto Discovery for Home-assistant 
SENSOR_NAME = "System Update"  # Sensor name
UNIQUE_ID = "system_update_sensor"  # Unique name for sensor

def get_upgradable_packages():
    # Update first and get upgradable list of applications 
    result = subprocess.run(["sudo", "apt", "update"], capture_output=True, text=True)
    result = subprocess.run(["sudo", "apt", "list", "--upgradable"], capture_output=True, text=True)
    lines = result.stdout.splitlines()

    packages = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 3:
            package_info = {
                "package": parts[0].split('/')[0],  # Packet name
                "current_version": parts[1],  # Current version
                "new_version": parts[2],  # New Version
            }
            packages.append(package_info)

    # JSON template
    update_info = {
        "total_upgradable": len(packages),
        "packages": packages
    }
    return update_info

def publish_update_info(update_info):
    client = mqtt.Client()
    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    # Auto Discovery message for home-assistant 
    sensor_config = {
        "name": SENSOR_NAME,
        "state_topic": f"{DISCOVERY_PREFIX}/sensor/system_update/state",
        "json_attributes_topic": f"{DISCOVERY_PREFIX}/sensor/system_update/state",  # JSON 
        "unique_id": UNIQUE_ID,
        "device": {
            "identifiers": ["system_update_device"],
            "name": "System Update Device",
            "manufacturer": "Your Manufacturer",
            "model": "Model X",
            "sw_version": "1.0"
        },
        "unit_of_measurement": "updates",  # Upgradable Packet list
        "value_template": "{{ value_json.total_upgradable }}"  # JSON Upgradable list of application
    }

    # Auto Discovery message for home-assistant 
    client.publish(f"{DISCOVERY_PREFIX}/sensor/system_update/config", json.dumps(sensor_config))
    time.sleep(1)  # delay for mqtt

    # Update date for sensor 
    client.publish(f"{DISCOVERY_PREFIX}/sensor/system_update/state", json.dumps(update_info))
    client.disconnect()

# Main Fuction
if __name__ == "__main__":
    update_info = get_upgradable_packages()
    publish_update_info(update_info)
    print("Update info published:", update_info)

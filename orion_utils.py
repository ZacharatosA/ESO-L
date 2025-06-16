import requests
import json
import os
from datetime import datetime

# Global variable to store the backup folder name
backup_folder = None

def get_backup_folder():
    """
    Get the backup folder for storing JSON files
    Returns:
        str: The path to the backup folder
    """
    # Create main Backup directory if it doesn't exist
    if not os.path.exists('Backup'):
        os.makedirs('Backup')
    return 'Backup'

def send_to_orion(url, fiware_service, fiware_path, modbus_id, type_name, value, value_type="Array"):
    """
    Send data to Orion Context Broker
    Args:
        url: The Orion endpoint (e.g. http://localhost:1026/v2/entities)
        fiware_service: The FIWARE service name
        fiware_path: The FIWARE service path
        modbus_id: The ID of the Modbus device
        type_name: The type of the data (e.g. 'coils', 'input_registers', 'holding_registers')
        value: The value to send
        value_type: The type of the value (default: "Array")
    """
    headers = {
        'Content-Type': 'application/json',
        'fiware-service': fiware_service,
        'fiware-servicepath': f'/{fiware_path}'
    }
    
    # Check if entity exists
    check_url = f"{url}/{modbus_id}"
    response = requests.get(check_url, headers=headers)
    
    if response.status_code == 404:  # Entity doesn't exist, create new
        data = {
            "id": modbus_id,
            "type": "ModbusDevice",
            type_name: {
                "type": value_type,
                "value": value
            }
        }
        response = requests.post(url, headers=headers, json=data)
        print(f"Created new entity. Response: {response.status_code}")
    else:  # Entity exists, update attribute
        # Use batch operation to add new attribute
        batch_url = f"{url.replace('/entities', '/op/update')}"
        data = {
            "actionType": "append",
            "entities": [
                {
                    "id": modbus_id,
                    "type": "ModbusDevice",
                    type_name: {
                        "type": value_type,
                        "value": value
                    }
                }
            ]
        }
        response = requests.post(batch_url, headers=headers, json=data)
        print(f"Updated existing entity. Response: {response.status_code}")
    
    return response.status_code

def save_to_json(data_type, data):
    """
    Save Modbus data to a JSON file in the Backup folder
    Args:
        data_type: Type of data (coils, input_registers, holding_registers)
        data: The data to save
    """
    # Get the backup folder
    folder = get_backup_folder()
    
    # Create filename
    filename = f'{folder}/{data_type}.json'
    
    # Prepare new data
    new_data = {
        'type': data_type,
        'timestamp': datetime.now().strftime('%Y.%m.%d_%H.%M.%S'),
        'values': list(data.bits) if data_type == 'coils' else data.registers
    }
    
    # Read existing data if file exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    
    # Append new data
    existing_data.append(new_data)
    
    # Save updated data back to file
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print(f"Data appended to {filename}")

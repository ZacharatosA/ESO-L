import requests
import json
import os
from datetime import datetime

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
    # Create Backup directory if it doesn't exist
    if not os.path.exists('Backup'):
        os.makedirs('Backup')
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'Backup/{data_type}_{timestamp}.json'
    
    # Prepare data for JSON
    if data_type == 'coils':
        json_data = {
            'type': data_type,
            'timestamp': timestamp,
            'values': list(data.bits[0:9])  # Convert to list directly
        }
    else:  # input_registers or holding_registers
        json_data = {
            'type': data_type,
            'timestamp': timestamp,
            'values': data.registers[0:9]
        }
    
    # Save to JSON file
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)
    print(f"Data saved to {filename}")

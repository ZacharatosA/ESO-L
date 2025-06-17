import requests
import json
import os
from datetime import datetime
import logging

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'logs')

# Setup logging to file
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global variable to store the backup folder name
backup_folder = None

def get_backup_folder():
    """
    Get the backup folder for storing JSON files
    Returns:
        str: The path to the backup folder
    """
    try:
        # Create main Backup directory if it doesn't exist
        backup_path = os.path.join(script_dir, 'Backup')
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
        return backup_path
    except Exception as e:
        logger.error(f"Error creating Backup directory: {e}")
        raise

def send_to_orion(url, fiware_service, fiware_path, entity_id, type_name, value, value_type="Array"):
    """
    Send data to Orion Context Broker
    Args:
        url: The Orion endpoint (e.g. http://localhost:1026/v2/entities)
        fiware_service: The FIWARE service name
        fiware_path: The FIWARE service path
        entity_id: The ID of the Modbus device
        type_name: The type of the data (e.g. 'coils', 'input_registers', 'holding_registers')
        value: The value to send
        value_type: The type of the value (default: "Array")
    """
    try:
        headers = {
            'Content-Type': 'application/json',
            'fiware-service': fiware_service,
            'fiware-servicepath': f'/{fiware_path}'
        }
        
        # Get current timestamp in ISO 8601 format
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        
        # Check if entity exists
        check_url = f"{url}/{entity_id}"
        response = requests.get(check_url, headers=headers)
        
        if response.status_code == 404:  # Entity doesn't exist, create new
            data = {
                "id": entity_id,
                "type": "ModbusDevice",
                type_name: {
                    "type": value_type,
                    "value": value,
                    "metadata": {
                        "timestamp": {
                            "type": "DateTime",
                            "value": current_time
                        }
                    }
                }
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 201:
                logger.error(f"Failed to create entity {entity_id}. Response: {response.status_code}")
        else:  # Entity exists, update attribute
            # Use batch operation to add new attribute
            batch_url = f"{url.replace('/entities', '/op/update')}"
            data = {
                "actionType": "append",
                "entities": [
                    {
                        "id": entity_id,
                        "type": "ModbusDevice",
                        type_name: {
                            "type": value_type,
                            "value": value,
                            "metadata": {
                                "timestamp": {
                                    "type": "DateTime",
                                    "value": current_time
                                }
                            }
                        }
                    }
                ]
            }
            response = requests.post(batch_url, headers=headers, json=data)
            if response.status_code != 204:
                logger.error(f"Failed to update entity {entity_id}. Response: {response.status_code}")
        
        return response.status_code
    except Exception as e:
        logger.error(f"Failed to send data to Orion: {e}")
        raise

def save_to_json(server_name, data, slave_name):
    """
    Save Modbus data to a JSON file in the Backup folder
    Args:
        server_name: Name of the server (e.g. 'SERVER1')
        data: The data to save
        slave_name: Name of the slave (e.g. 'SLAVE1')
    """
    try:
        # Get the backup folder
        folder = get_backup_folder()
        
        # Create filename
        filename = f'{folder}/{server_name}.json'
        
        # Prepare new data
        new_data = {
            'type': slave_name,
            'timestamp': datetime.now().strftime('%Y.%m.%d_%H.%M.%S'),
            'values': list(data.bits) if 'coils' in slave_name.lower() else data.registers
        }
        
        # Read existing data if file exists
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
                except json.JSONDecodeError:
                    logger.warning(f"Could not decode existing JSON, starting fresh")
                    existing_data = []
        else:
            existing_data = []
        
        # Append new data
        existing_data.append(new_data)
        
        # Save updated data back to file
        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=4)
            
    except Exception as e:
        logger.error(f"Failed to save data to JSON: {e}")
        raise 
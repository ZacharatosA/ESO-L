from pymodbus.client import ModbusTcpClient
from orion_utils import send_to_orion, save_to_json
import configparser
import time

def read_registers(client, address_start, data_size, slave_id):
    result = client.read_holding_registers(address=address_start, count=data_size, slave=slave_id)
    print(result.registers)
    if LOCAL_SAVE:
        save_to_json('holding_registers', result)
    send_to_orion(ORION_URL, FIWARE_SERVICE, FIWARE_SERVICEPATH, ENTITY_ID, 'holding_registers', result.registers, "Array")
    return result

# Read configuration
config = configparser.ConfigParser()
config.read('config.conf')
# Get Modbus configuration
MODBUS_IP = config.get('DEFAULT', 'modbus_ip')
MODBUS_PORT = config.getint('DEFAULT', 'modbus_port')
DATA_SIZE = config.getint('DEFAULT', 'data_size')
ADDRESS_START = config.getint('DEFAULT', 'address_start')
RATE = config.getint('DEFAULT', 'rate')  # Executions per minute
SLAVE_ID = config.getint('DEFAULT', 'slave_id')
# Get Orion configuration
ORION_URL = config.get('DEFAULT', 'orion_url')
FIWARE_SERVICE = config.get('DEFAULT', 'fiware_service')
FIWARE_SERVICEPATH = config.get('DEFAULT', 'fiware_servicepath')
ENTITY_ID = config.get('DEFAULT', 'entity_id')
# Get Local Storage configuration
LOCAL_SAVE = config.getboolean('DEFAULT', 'local_save')

def main():
    sleep_time = 60 / RATE  # Convert executions per minute to seconds between executions
    while True:
        client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)
        client.connect()

        read_registers(client, ADDRESS_START, DATA_SIZE, SLAVE_ID)
        
        client.close()
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
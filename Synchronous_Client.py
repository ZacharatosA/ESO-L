from pymodbus.client import ModbusTcpClient
from orion_utils import send_to_orion, save_to_json
import configparser


# Read configuration
config = configparser.ConfigParser()
config.read('config.conf')
# Get Modbus configuration
MODBUS_IP = config.get('DEFAULT', 'MODBUS_IP')
MODBUS_PORT = config.getint('DEFAULT', 'MODBUS_PORT')
DATA_SIZE = config.getint('DEFAULT', 'DATA_SIZE')
# Get Orion configuration
ORION_URL = config.get('DEFAULT', 'ORION_URL')
FIWARE_SERVICE = config.get('DEFAULT', 'FIWARE_SERVICE')
FIWARE_SERVICEPATH = config.get('DEFAULT', 'FIWARE_SERVICEPATH')
ENTITY_ID = config.get('DEFAULT', 'ENTITY_ID')
# Get Local Storage configuration
LOCAL_SAVE = config.getboolean('DEFAULT', 'LOCAL_SAVE')

# Synchronous Client ----------------------------------------------------------------------------------------------
client = ModbusTcpClient(MODBUS_IP, port=MODBUS_PORT)       # Create client object
client.connect()                                            # connect to device
client.write_coil(address=3, value=True, slave=1)           # set information in device
result1 = client.read_coils(address=0, count=DATA_SIZE, slave=1)   # get information from device
print(result1.bits)   
if LOCAL_SAVE:
    save_to_json('coils', result1)
send_to_orion(ORION_URL, FIWARE_SERVICE, FIWARE_SERVICEPATH, ENTITY_ID, 'coils', result1.bits, "Array")

result2 = client.read_input_registers(address=0, count=DATA_SIZE, slave=2)    # get information from device
print(result2.registers) 
if LOCAL_SAVE:
    save_to_json('input_registers', result2)
send_to_orion(ORION_URL, FIWARE_SERVICE, FIWARE_SERVICEPATH, ENTITY_ID, 'input_registers', result2.registers, "Array")

client.write_register(address=3, value=15, slave=3)           # set information in device
result3 = client.read_holding_registers(address=0, count=DATA_SIZE, slave=3)    # get information from device
print(result3.registers) 
if LOCAL_SAVE:
    save_to_json('holding_registers', result3)
send_to_orion(ORION_URL, FIWARE_SERVICE, FIWARE_SERVICEPATH, ENTITY_ID, 'holding_registers', result3.registers, "Array")

client.close()
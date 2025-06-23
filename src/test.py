from pymodbus.client import ModbusTcpClient

# client = ModbusTcpClient("172.25.64.1", port=502)
# client.connect()
# result1 = client.read_holding_registers(address=0, count=1, slave=1)
# print(result1.registers)
# client.close()

client = ModbusTcpClient("172.25.64.1", port=503)
client.connect()
result2 = client.read_holding_registers(address=0, count=5, slave=1)
print(result2.registers)
client.close()


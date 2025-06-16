from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient("172.25.64.1", port=503)
client.connect()
result1 = client.read_holding_registers(address=0, count=3, slave=2)
result2 = client.read_holding_registers(address=0, count=3, slave=3)
client.close()
print(result1.registers)
print(result2.registers)
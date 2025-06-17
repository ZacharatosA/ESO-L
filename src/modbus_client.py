from pymodbus.client import ModbusTcpClient
import logging

logger = logging.getLogger(__name__)

class ModbusClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = None
    
    def connect(self):
        """Connect to Modbus device"""
        try:
            self.client = ModbusTcpClient(self.ip, port=self.port)
            self.client.connect()
            logger.info(f"Connected to Modbus device at {self.ip}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Modbus device: {e}")
            raise
    
    def read_registers(self, address_start, data_size, slave_id):
        """Read holding registers from Modbus device"""
        try:
            result = self.client.read_holding_registers(address=address_start, count=data_size, slave=slave_id)
            return result
        except Exception as e:
            logger.error(f"Failed to read registers: {e}")
            raise
    
    def close(self):
        """Close connection to Modbus device"""
        if self.client:
            self.client.close() 
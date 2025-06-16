import time
import logging
from config_manager import ConfigManager
from modbus_client import ModbusClient
import orion_utils

class ModbusMonitor:
    def __init__(self):
        self.config = ConfigManager()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def read_registers(self, client, address_start, data_size, slave_id, server_name, slave_name):
        try:
            result = client.read_registers(
                address_start,
                data_size,
                slave_id
            )
            
            if result.isError():
                self.logger.error(f"Error reading from {server_name}.{slave_name}: {result}")
                return None
                
            self.logger.info(f"Read from {server_name}.{slave_name}: {result.registers}")
            
            # Save locally if enabled
            if self.config.get_storage_config()['local_save']:
                orion_utils.save_to_json(server_name, result, slave_name)
            
            # Send to Orion
            orion_config = self.config.get_orion_config()
            entity_id = self.config.get_server_config(server_name)['entity_id']
            orion_utils.send_to_orion(
                orion_config['url'],
                orion_config['service'],
                orion_config['servicepath'],
                entity_id,
                f"{slave_name}_registers",
                result.registers,
                "Array"
            )
            
            return result
        except Exception as e:
            self.logger.error(f"Error processing {server_name}.{slave_name}: {e}")
            return None
    
    def process_server(self, server_name):
        try:
            # Get server configuration
            server_config = self.config.get_server_config(server_name)
            client = ModbusClient(server_config['ip'], server_config['port'])
            client.connect()
            
            # Get all slaves for this server
            slaves = self.config.get_server_slaves(server_name)
            
            # Process each slave
            for slave_name, slave_config in slaves.items():
                self.read_registers(
                    client,
                    slave_config['address_start'],
                    slave_config['data_size'],
                    slave_config['slave_id'],
                    server_name,
                    slave_name
                )
            
            client.close()
        except Exception as e:
            self.logger.error(f"Error processing server {server_name}: {e}")
    
    def run(self):
        while True:
            try:
                # Get all servers
                servers = self.config.get_servers()
                
                # Process each server
                for server_name in servers:
                    self.process_server(server_name)
                
                # Wait for next execution
                rate = self.config.get_rate()
                sleep_time = 60 / rate  # Convert executions per minute to seconds
                time.sleep(sleep_time)
                
            except KeyboardInterrupt:
                self.logger.info("Program terminated by user")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    monitor = ModbusMonitor()
    monitor.run() 
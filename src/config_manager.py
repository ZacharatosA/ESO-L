import configparser
import os

# Configuration Manager Class - Handles loading and reading settings from config.conf file
# Provides methods to access Modbus connection parameters (IP, port, slave IDs, register addresses)
# as well as Orion Context Broker settings and general application settings (rate, local_save)
class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        # Get the project root directory (two levels up from src)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'App_Config', 'config.conf')
        self.config.read(config_path)
    
    def get_orion_config(self):
        """Get Orion Context Broker configuration"""
        return {
            'url': self.config.get('ORION_CONFIG', 'orion_url'),
            'service': self.config.get('ORION_CONFIG', 'fiware_service'),
            'servicepath': self.config.get('ORION_CONFIG', 'fiware_servicepath')
        }
    
    def get_storage_config(self):
        """Get local storage configuration"""
        return {
            'local_save': self.config.getboolean('GENERAL', 'local_save')
        }
    
    def get_rate(self):
        """Get execution rate"""
        return self.config.getint('GENERAL', 'rate')
    
    def get_servers(self):
        """Get list of all server names"""
        return [section for section in self.config.sections() 
                if section.startswith('SERVER') and '.' not in section]
    
    def get_server_config(self, server_name):
        """Get configuration for a specific server"""
        return {
            'ip': self.config.get(server_name, 'modbus_ip'),
            'port': self.config.getint(server_name, 'modbus_port'),
            'entity_id': self.config.get(server_name, 'entity_id')
        }
    
    def get_server_slaves(self, server_name):
        """Get all slaves for a specific server"""
        slaves = {}
        for section in self.config.sections():
            if section.startswith(f"{server_name}.SLAVE"):
                slave_name = section.split('.')[-1]
                slaves[slave_name] = {
                    'slave_id': self.config.getint(section, 'slave_id'),
                    'address_start': self.config.getint(section, 'address_start'),
                    'data_size': self.config.getint(section, 'data_size')
                }
        return slaves 
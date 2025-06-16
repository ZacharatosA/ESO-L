# Modbus Monitor (OOP Version)

A Python application for monitoring Modbus devices using Object-Oriented Programming principles.

## Features

- Multiple slave support
- Configurable execution rate
- Local data storage
- Orion Context Broker integration
- Robust error handling
- Logging system

## Installation

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.conf` to set up:
- Modbus device connection
- Slave configurations
- Orion Context Broker settings
- Execution rate
- Local storage options

## Usage

Run the application:
```bash
python Synchronous_Client.py
```

The program will:
1. Connect to the Modbus device
2. Read data from configured slaves
3. Save data locally (if enabled)
4. Send data to Orion Context Broker
5. Wait for the configured rate before repeating

## Project Structure

- `config.conf`: Configuration file
- `config_manager.py`: Configuration management
- `modbus_client.py`: Modbus communication
- `Synchronous_Client.py`: Main application
- `orion_utils.py`: Orion Context Broker utilities
- `requirements.txt`: Python dependencies 
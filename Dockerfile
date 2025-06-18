# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files
COPY src/ ./src/

# Create data directory for logs and backups
RUN mkdir -p /app/data/logs /app/data/Backup

# Create mount point for App_Config
VOLUME ["/app/App_Config"]

# Set Python path
ENV PYTHONPATH=/app

# Command to run the application
CMD ["python", "src/Synchronous_Client.py"] 
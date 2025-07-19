#!/bin/bash

# Railway startup script for Car Store application
# This script handles port configuration and starts the application

# Set default port if PORT is not set
if [ -z "$PORT" ]; then
    export PORT=8000
    echo "PORT not set, using default: $PORT"
else
    echo "Using PORT from environment: $PORT"
fi

# Validate that PORT is a number
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: PORT '$PORT' is not a valid number, using default 8000"
    export PORT=8000
fi

echo "Starting Car Store application on port $PORT..."
echo "Command: gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app"

# Start the application with gunicorn
exec gunicorn --bind "0.0.0.0:$PORT" --timeout 120 --workers 1 app:app
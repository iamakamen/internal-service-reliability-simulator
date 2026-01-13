#!/bin/bash

# PID file to store the process ID
PID_FILE="/tmp/app_service.pid"

# Function to stop the service
stop_service() {
    echo "Stopping service..."
    
    # Kill process using port 5000
    if command -v lsof &> /dev/null; then
        PID=$(lsof -ti:5000 2>/dev/null)
        if [ -n "$PID" ]; then
            kill "$PID" 2>/dev/null || true
            echo "Killed process on port 5000 (PID: $PID)"
        fi
    fi
    
    # Also check PID file
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID" 2>/dev/null || true
            echo "Killed service (PID: $PID)"
        fi
        rm -f "$PID_FILE"
    fi
    
    # Fallback: kill by process name
    pkill -f "python app/app.py" 2>/dev/null || true
    echo "Service stopped"
}

# Check for command line argument
case "$1" in
    stop)
        stop_service
        exit 0
        ;;
    restart)
        stop_service
        sleep 1
        ;;
    *)
        # Default: start the service
        ;;
esac

echo "Starting service..."
export SERVICE_DB_PATH=data/service.db
python app/app.py &
APP_PID=$!
echo "$APP_PID" > "$PID_FILE"
echo "Service started (PID: $APP_PID)"

sleep 2

echo "Running health check..."
python scripts/health_check.py

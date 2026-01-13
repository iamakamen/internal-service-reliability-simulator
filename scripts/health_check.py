import requests
import sys
import os

SERVICE_URL = "http://localhost:5000/metrics"
LOG_FILE = "logs/service.log"

def check_service():
    try:
        response = requests.get(SERVICE_URL, timeout=2)
        if response.status_code != 200:
            print("FAIL: /metrics returned non-200")
            return False
        return True
    except Exception as e:
        print(f"FAIL: Service unreachable - {e}")
        return False

def check_logs():
    if not os.path.exists(LOG_FILE):
        print("FAIL: Log file missing")
        return False

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()[-20:]

    for line in lines:
        if "ERROR" in line or "Exception" in line:
            print("FAIL: Error found in logs")
            return False

    return True

if __name__ == "__main__":
    if not check_service():
        sys.exit(1)

    if not check_logs():
        sys.exit(1)

    print("OK: Service healthy")
    sys.exit(0)

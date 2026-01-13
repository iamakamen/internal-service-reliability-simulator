## Incident 1: Missing Configuration Variable

Summary:
The service failed to retrieve shipment metrics due to a missing database path configuration.

Detection:
The issue was detected when the /metrics endpoint returned HTTP 500 responses.

Root Cause:
The SERVICE_DB_PATH environment variable was not set, causing database connection initialization to fail.

Mitigation:
The environment variable was restored and the service restarted.

Prevention:
Add a startup configuration validation step and improve monitoring to detect misconfiguration earlier.



## Incident 2: Log File Permission Denied

Summary:
The service failed to process requests due to insufficient permissions to write to the log file.

Detection:
The issue was detected when the /metrics endpoint returned HTTP 500 responses and a permission error was observed during request handling.

Root Cause:
The log file had read-only permissions, preventing the service from appending log entries.

Mitigation:
File permissions were corrected to allow write access, and the service was restarted.

Prevention:
Add startup checks for file write permissions and run the service under a user with verified access rights.




## Incident 3: SQL Schema Mismatch

Summary:
The metrics endpoint failed due to a mismatch between the application query and the database schema.

Detection:
The issue was detected when the /metrics endpoint returned HTTP 500 responses and an SQL error was observed during request handling.

Root Cause:
The application queried a non-existent column due to a schema mismatch.

Mitigation:
The query was corrected to align with the existing database schema.

Prevention:
Introduce schema validation checks and controlled migration processes to prevent version skew between application code and database schema.

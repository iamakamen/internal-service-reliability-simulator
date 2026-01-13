# Internal Service Reliability Simulator

## Overview

This project simulates the operation and support of an internal production service similar to those used in large-scale transportation and logistics platforms.

The system exposes a simple HTTP endpoint that serves operational metrics backed by a relational database. The primary focus of this project is service reliability, incident handling, monitoring, and operational automation rather than feature development.

The project was intentionally designed to:

* Fail in realistic ways
* Surface clear diagnostic signals
* Be repaired without data loss
* Demonstrate production engineering judgment

## System Architecture

The system consists of the following components:

* **HTTP Service**
    A Python Flask application exposing a `/metrics` endpoint.
* **Database Layer**
    SQLite database storing shipment records and supporting aggregation queries.
* **Configuration Layer**
    Environment-based configuration for database connectivity.
* **Logging Layer**
    File-based logging with graceful fallback to stdout when file logging is unavailable.
* **Monitoring Script**
    A health check script that proactively detects service degradation.
* **Automation Script**
    A restart and verification script to reduce manual operational effort.

A high-level logical architecture diagram is available under `docs/architecture/`.

### High-level flow:

1.  Client calls `/metrics`
2.  Service queries the database
3.  Results are returned as JSON
4.  Logs and health signals are emitted for observability

## Incidents Handled

This project intentionally introduced and resolved multiple production-grade incidents.

### Incident 1: Missing Configuration Variable

* **Failure:** Database path environment variable not set
* **Impact:** `/metrics` returned HTTP 500
* **Detection:** Error surfaced via logs and failed request
* **Root Cause:** Missing runtime configuration
* **Mitigation:** Restore environment variable and restart service
* **Prevention:** Startup validation and configuration checks

### Incident 2: Log File Permission Denied

* **Failure:** Log file lacked write permissions
* **Impact:** Service crashed at startup
* **Detection:** `PermissionError` surfaced in stdout
* **Root Cause:** Logging initialisation attempted to open a read-only file
* **Mitigation:** Implemented resilient logging with stdout fallback
* **Prevention:** Defensive logging setup and permission checks

This incident highlighted the difference between startup-time failures and request-time failures, a critical operational distinction.

### Incident 3: SQL Schema Mismatch

* **Failure:** Application queried a non-existent database column
* **Impact:** `/metrics` returned HTTP 500 while service remained running
* **Detection:** `sqlite3.OperationalError` during request handling
* **Root Cause:** Application and database schema mismatch
* **Mitigation:** Corrected query to match schema
* **Prevention:** Controlled schema migrations and validation checks

## Monitoring

A proactive monitoring script is provided at:

`scripts/health_check.py`

The health check verifies:

* Service reachability
* HTTP 200 response from `/metrics`
* Successful database query execution
* Absence of recent error signals in logs

The script exits with:

* `0` for healthy state
* `1` for unhealthy state

This design makes it suitable for cron jobs, CI pipelines, or internal monitoring systems.

## Automation

Operational automation is provided via:

`scripts/restart_service.sh`

### Capabilities:

* Graceful service stop using PID tracking
* Safe restart with environment reinitialisation
* Post-restart health verification
* Fallback termination logic if PID information is missing

This reduces manual recovery effort and mirrors real-world on-call recovery tooling.

## Execution Evidence

Supporting screenshots documenting failures, diagnosis, and recovery
are available under:

evidence/screenshots/

They are organised by project phase and incident type to preserve
a clear operational timeline.

## To-Do and Future Improvements

Given more time, the following improvements would be prioritised:

 - [] Add startup-time validation for database schema compatibility
 - [] Replace manual process management with systemd unit files
 - [] Introduce structured JSON logging for easier aggregation
 - [] Add request latency tracking to monitoring signals
 - [] Implement controlled schema migration tooling
 - [] Add basic authentication to the metrics endpoint
 - [] Extend monitoring to detect abnormal metric trends

These enhancements would further harden the system for long-term production use.

## Summary

This project demonstrates:

* Realistic incident handling
* Linux and process-level debugging
* SQL failure diagnosis
* Proactive monitoring design
* Operational automation
* Clear documentation and evidence

The emphasis throughout is on reliability, observability, and ownership, not feature complexity.

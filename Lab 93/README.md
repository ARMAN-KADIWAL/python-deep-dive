# Lab 93 — Applying Design Patterns in Practice

A simulated notification system refactored using Factory and Singleton patterns. The code is a reconstructed, condensed implementation of the supplied lab with missing imports fixed, shared configuration wired to notification classes, singleton initialization protected, and simulated credentials not printed.

## Run

```bash
python3 original_notification_system.py
python3 notification_logger.py
python3 refactored_notification_system.py
python3 -m unittest -v test_notification_system.py
```

Email, SMS, push and Slack operations are simulations, not actual network deliveries. JSON files are generated locally and ignored by Git. The timeout, retry and log-level settings are illustrative; they do not control real network operations. Only singleton initialization and logger data access are protected by locks, not every configuration mutation. Tests are included; execution status must be verified separately.

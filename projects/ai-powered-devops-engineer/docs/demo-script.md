# Five-Minute Demo Script

## 0:00 to 0:30 - Explain the problem
Application logs contain signals, but repeated errors and bursts take time to triage. This tool turns logs into evidence-backed findings before optional AI diagnosis.

## 0:30 to 1:15 - Start the app
Run Streamlit locally and open the local URL. Explain that the default path does not require AWS credentials.

## 1:15 to 2:00 - Analyze a synthetic incident
Choose Database connection failure and click Analyze logs. Show parsed event counts, warning/error totals, repeated fingerprints, and error burst findings.

## 2:00 to 3:00 - Inspect evidence
Open a finding. Explain that the tool reports source line numbers, severity rules, counts, and limitations. The finding is a signal, not proof of root cause.

## 3:00 to 3:45 - Generate a report
Download the JSON and Markdown reports. Explain how machine-readable reports can be used in issue templates or later automation.

## 3:45 to 4:30 - Demonstrate AI boundary
Run the offline diagnosis and show the explicit demo label. If using Bedrock, confirm model configuration and consent first; explain that sanitized log evidence leaves the machine and the call may incur charges.

## 4:30 to 5:00 - Discuss engineering decisions
Highlight deterministic-first analysis, optional cloud dependencies, input size bounds, redaction, no automatic remediation, and unit tests.

Do not claim an AWS deployment, test result, cost saving, or verified root cause unless it has actually been demonstrated.

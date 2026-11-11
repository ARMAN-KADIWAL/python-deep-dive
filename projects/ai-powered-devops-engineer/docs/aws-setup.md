# AWS Setup: Read-Only CloudWatch Logs

CloudWatch is optional. The application works locally without AWS credentials. This guide does not create AWS resources.

## Before starting

- Choose an existing log group that you are authorized to inspect.
- Confirm the AWS Region.
- Use an existing named profile or IAM role rather than pasting keys into source code.
- Check current CloudWatch Logs pricing and account-specific charges before use.
- Do not use sensitive production log data in a portfolio demo.

## Permission scope

The adapter currently calls FilterLogEvents for the one log group the operator enters. The sample policy is in infra/iam/cloudwatch-readonly-policy.json.

Replace REGION, ACCOUNT_ID, and LOG_GROUP_NAME with the exact values for the intended log group. Validate the ARN format for your account and partition. The policy intentionally does not grant log-group creation, deletion, subscription changes, or log ingestion permissions.

The relevant IAM action is logs:FilterLogEvents, which supports log-group-level resource scope. Verify the current AWS Service Authorization Reference and API documentation before using the policy in a real account.

## Local credential configuration

For a pre-existing AWS CLI profile, set the profile before launching the app.

PowerShell:

    $env:AWS_PROFILE = "your-existing-profile"
    $env:AWS_REGION = "ap-south-1"
    $env:DEVOPS_AI_BEDROCK_ENABLED = "false"
    streamlit run app.py

Bash:

    export AWS_PROFILE="your-existing-profile"
    export AWS_REGION="ap-south-1"
    export DEVOPS_AI_BEDROCK_ENABLED=false
    streamlit run app.py

The profile must already be configured locally. Do not commit profile files or credentials. The application intentionally does not print credential values.

## Use the dashboard

1. Select AWS CloudWatch Logs.
2. Enter the existing log group name.
3. Select a bounded lookback period.
4. Confirm the read-only API request.
5. Select Fetch and analyze CloudWatch events.
6. Inspect parsed events and findings.

The UI fetches at most 500 events. The adapter validates the date range and event limit, and handles continuation tokens. If no events are returned, verify the log group, Region, time range, and permissions.

## Troubleshooting

- AccessDenied: verify logs:FilterLogEvents permission and the resource ARN.
- Resource not found: verify the group name and Region.
- Invalid credentials: reconfigure the existing local profile or role.
- Empty response: widen the lookback period within the UI's maximum and confirm events exist.
- No credentials: continue using synthetic samples; AWS access is optional.

No cloud resources are provisioned by this project. Do not create or attach administrator policies to make the integration work.

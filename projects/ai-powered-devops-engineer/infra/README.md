# Infrastructure Folder

This folder contains optional AWS configuration examples for learning and controlled future integration.

- iam/cloudwatch-readonly-policy.json is a policy template for the currently implemented CloudWatch FilterLogEvents reader. Replace its placeholders and review its scope before use.

No AWS resources are created by local setup. There are no Terraform or CloudFormation stacks in this milestone. Before adding deployment templates, document each resource, its permissions, public exposure, current cost drivers, and exact cleanup steps. Never add account-specific IDs, credentials, or secrets to the repository.

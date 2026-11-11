# Deployment Guide

## Local run

Use Python 3.11 or later, create a virtual environment, install the development extra, and run Streamlit as described in the project README. Local log analysis does not require AWS credentials.

## Docker

Build from this project directory:

    docker build -t ai-powered-devops-engineer:local .
    docker run --rm -p 127.0.0.1:8501:8501 ai-powered-devops-engineer:local

The Compose configuration binds the dashboard to localhost by default. Do not bind it to a public interface without adding authentication and reviewing the threat model.

## Optional Amazon Bedrock

The adapter uses the AWS SDK credential provider chain. Before enabling it, confirm:
- The selected model is available to the AWS account and Region.
- The model supports the Converse API used by this adapter.
- The caller has only the required model invocation permission.
- The account has access to invoke the selected model.
- The operator has reviewed the data that may be sent to AWS.
- The applicable current AWS pricing and data handling terms.

Bedrock use can incur charges. This project does not create model endpoints or AWS resources.

## Future cloud deployment

Do not deploy publicly by default. Potential options include a small EC2 instance running Docker or a managed container platform. Compare current pricing, compute, storage, networking, logging, availability, authentication, and cleanup before selecting one. Prices and free-tier eligibility change; use current official AWS pricing pages and the AWS Pricing Calculator.

No AWS infrastructure is provisioned by this repository. Obtain explicit approval and review the exact resource plan before creating anything.

## Cleanup

For a local container, stop it with Ctrl+C or stop the Compose service. Remove only the local image if no longer needed. Since this version creates no AWS resources, there is no AWS stack to delete.

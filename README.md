# A Collection of Extension Functions Based on Boto3

## Supported CLI Commands

### DynamoDB Commands
- **truncate-table**: Truncate a DynamoDB table by deleting all its items.

### S3 Commands
- **delete-bucket**: Clean and delete an S3 bucket completely, including all objects and versions.
- **ls**: List all objects in an S3 bucket.

### Route 53 Commands
- **export-hosted-zone**: Export all resource record sets from a specified hosted zone.
- **import-hosted-zone**: Import resource record sets into a specified hosted zone from a file, skipping NS and SOA records.


### SageMaker Commands
- **human-effort**: Generate a report on the human effort that a SageMaker job required.


## Development Environment Quickstart

```pwsh
uv sync
uv run botobuddy --help
```

# A Collection of Extension Functions Based on Boto3

## Development Environment Quickstart

```pwsh
uv sync
uv run cli.py --help
```

## Supported Commands

### DynamoDB Commands
- **truncate-table**: Truncate a DynamoDB table by deleting all its items.

### S3 Commands
- **delete-bucket**: Clean and delete an S3 bucket completely, including all objects and versions.

### Route 53 Commands
- **export-hosted-zone**: Export all resource record sets from a specified hosted zone.
- **import-hosted-zone**: Import resource record sets into a specified hosted zone from a file, skipping NS and SOA records.

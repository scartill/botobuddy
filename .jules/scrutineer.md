## Architectural Traps
- **Redundant Exception Wrapping**: The project contains instances where generic `boto3` or `botocore` exceptions are caught and wrapped in a `UserWarning`. This is a trap because it obfuscates the original stack trace and AWS error codes, making debugging harder. Native `ClientError` should bubble up naturally.

# Botobuddy Project Context

`botobuddy` is a Python-based AWS utility CLI designed to provide high-level, opinionated extensions to the standard `boto3` library. It simplifies common but multi-step AWS operations such as bucket cleaning, DynamoDB table truncation, and Route 53 record management.

## Project Structure

- **`src/botobuddy/`**: Core package containing all logic.
    - **`cli.py`**: The main entry point using `click`. It handles global options (profile, region, role assumption) and dynamically imports commands from service-specific modules.
    - **`common.py`**: Centralized AWS session and client/resource factory logic. Handles AWS profile selection, region configuration, and STS role assumption.
    - **`logger.py`**: Logging configuration using `rich` for formatted output.
    - **`utils.py`**: General-purpose utility functions (e.g., `dslice` for dictionary manipulation).
    - **Service Modules**:
        - `s3.py`: S3 operations (delete bucket, fast parallel downloads, sync).
        - `dynamo.py`: DynamoDB operations (truncate table).
        - `route53.py`: Route 53 operations (export/import hosted zones).
        - `sagemaker.py`: SageMaker related utilities.
        - `apigw.py`, `awslambda.py`, `secman.py`: Utilities for API Gateway, Lambda, and Secrets Manager.
- **`pyproject.toml`**: Project metadata, dependencies (`boto3`, `click`, `python-benedict`, `rich`), and script definitions.
- **`uv.lock`**: Managed by `uv` for reproducible environments.

## Technical Stack

- **Language**: Python 3.12+
- **AWS SDK**: `boto3` with `types-boto3` for robust type hinting.
- **CLI Framework**: `click`
- **Data Manipulation**: `python-benedict` for advanced dictionary/JSON/YAML/TOML handling.
- **Environment Management**: `uv`

## Building and Running

The project uses `uv` for development and package management.

- **Install Dependencies**: `uv sync`
- **Run CLI Locally**: `uv run botobuddy [COMMAND]`
- **Build Package**: `uv build`
- **Publish**: Handled via `.github/workflows/publish.yml` (triggered on tags).

## Development Conventions

- **Modular Commands**: CLI commands are grouped by service. Each service module should implement an `import_commands(parent)` function to register its commands with the main CLI group.
- **AWS Session Handling**: Always use the factory functions in `botobuddy.common` (`get_s3_client`, `get_dynamodb_resource`, etc.) to ensure global CLI options like `--profile` or `--assume-role` are respected.
- **Type Safety**: Use `types-boto3` for all AWS client/resource interactions.
- **Logging**: Use `botobuddy.logger.logger` for all output. Avoid `print()` unless it's a direct command output intended for piping.
- **Error Handling**: Prefer raising `UserWarning` or descriptive exceptions that the main `cli.py` can catch and log appropriately. Use `--traceback` for debugging.
- **Testing**: (TODO: Implement a test suite. No `tests/` directory was found during initial analysis).

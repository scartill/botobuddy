# 0.7.1

- Sentinel security fix: Added input length limit to request body

# 0.7.0

- Major refactoring of AWS client factories
- Enhanced CLI options for region and profile selection

# 0.6.0

- Added SSM Parameter Store client and `get_ssm_parameter` utility
- Added Lambda client support and `get_function_url` utility
- Added comprehensive docstrings across all modules
- Switched to `hatchling` build system
- Refactored `get_sub_to_email_mapping` to use boto3 paginator

# 0.5.3

- Fixed secure temp file creation and cleanup for `s3.download_file` in `view_dict_cmd`
- Added CI/CD workflow for publishing to PyPI
- Added `GEMINI.md` file with project context and conventions

# 0.5.2

- Security-related bugfixes (fixed path traversal in S3 object downloads)
- Removed redundant `list_objects_v2` loop in S3 bucket deletion

# 0.5.1

- Added add session config support to secrets manager client

# 0.5.0

- Added `botobuddy.awslambda.get_this_url` function

# 0.4.0

- Added `botobuddy.awslambda.response` function
- Added `botobuddy.awslambda.request_params` function
- Added `botobuddy.secman.get_sm_secret` function

# 0.3.8

- Fixed the `/` operator of the `botobuddy.s3.S3Uri` class
- Reduced the default `concurrency` parameter value to 10 for fast downloads

# 0.3.7

- Added the `/` operator to `botobuddy.s3.S3Uri` class
- Downgraded `click` to ">=8.1.0" to fix compatibility issues

# 0.3.6

- Enhanced logging
- Added parameters to `botobuddy.s3.sync_folder_from_s3` function:
    - `recursive`
    - `skip_existing`
    - `concurrency`
- Added `botobuddy s3 sync` command
- Fixed s3 client creation issue for `sync_folder_from_s3` function

# 0.3.5

- Added `recursive` parameter to `botobuddy.s3.sync_folder_from_s3` function

# 0.3.4

- Added `botobuddy.s3.sync_folder_from_s3` function

# 0.3.3

- Added `botobuddy s3 view-dict` command

# 0.3.2

- Downgraded `rich` to "13.0.0" to fix compatibility issues with `aws-sam-cli`
- Added `botobuddy --version` option

# 0.3.1

- Fixed fast download concurrency issue
- Added support for default session config values
- Increased S3 download concurrency from 10 to 100 in SageMaker
- Corrected core configuration handling

# 0.3.0

- Added `botobuddy.s3.S3Uri` class
- Added `botobuddy.utils.dslice` utility function
- Improved error handling and status checks for SageMaker labeling jobs

# 0.2.0

- Added project URL links to `pyproject.toml`
- Renamed session configuration parameters for better clarity
- Enhanced task progress tracking and decreased S3 download verbosity

# 0.1.0

- Initial release
- Added Route 53 resource record sets management
- Added DynamoDB table truncation support
- Added SageMaker human effort analysis command
- Added S3 fast download utility for parallel file downloads
- Added AWS role assumption support
- Added support for botocore session configuration
- Initial project configuration using `uv`

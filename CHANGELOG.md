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

# 0.3.0

- Add `botobuddy.s3.S3Uri` class
- Add `botobuddy.utils.dslice` function
- Add `botobuddy.sagemaker.analyse_human_effort` function

# 0.2.0

- Some interface refactoring

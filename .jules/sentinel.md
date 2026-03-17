## 2025-02-14 - Path Traversal (Zip Slip) in S3 Object Downloads
**Vulnerability:** S3 object keys with directory traversal characters (`../`) were directly joined with local directories to generate target file paths.
**Learning:** Python's `pathlib.Path.relative_to` combined with the `/` operator doesn't inherently protect against traversal characters embedded in the original string, leading to an absolute path resolution outside the target directory if unvalidated.
**Prevention:** Always use `.resolve()` on the final composed path and verify it is strictly contained within the intended base directory using `.is_relative_to(base_dir.resolve())`.

## 2025-03-17 - Sensitive Data Exposure in Logs (Assumed Role Credentials)
**Vulnerability:** The entire `assumed_role_object` returned by `sts.assume_role` was being logged at the `DEBUG` level. This object contains temporary AWS credentials (`AccessKeyId`, `SecretAccessKey`, `SessionToken`) in plain text.
**Learning:** Even debug logs can leak critical secrets if whole response objects from identity or authentication services are dumped indiscriminately.
**Prevention:** Always selectively log safe, non-sensitive attributes (like `AssumedRoleUser` details) from authentication/authorization responses instead of logging the entire payload.

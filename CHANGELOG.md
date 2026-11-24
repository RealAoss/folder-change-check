# Changelog

## Unreleased

- Added the MIT license, contribution instructions and continuous integration.

## Initial version

- Verify a folder after a backup, copy or restore. Save a SHA-256 fingerprint of each regular file, then compare the saved manifest with the copied folder. Names are relative to the scanned folder so the two locations can differ.

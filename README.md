# Folder Change Check

Verify a folder after a backup, copy or restore. Save a SHA-256 fingerprint of each regular file, then compare the saved manifest with the copied folder. Names are relative to the scanned folder so the two locations can differ.

```sh
python app.py save original manifest.json
python app.py check restored manifest.json
```

Requires Python 3.9+. Store the manifest outside the scanned folder. Save refuses to overwrite an existing manifest. The report lists added, removed and changed paths. Exit codes are 0 for a match or successful save, 1 for differences and 2 for errors. Empty directories, metadata and symbolic links are excluded.

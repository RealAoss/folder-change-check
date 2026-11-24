"""Save a folder fingerprint and compare it after copying or restoring files."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def fingerprint(root):
    if not root.is_dir():
        raise ValueError("Choose an existing folder")
    files = {}
    def fail(error):
        raise error
    for folder, subfolders, names in os.walk(root, onerror=fail):
        base = Path(folder)
        subfolders[:] = [n for n in subfolders if not (base / n).is_symlink()]
        for name in names:
            path = base / name
            if path.is_symlink() or not path.is_file():
                continue
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            files[path.relative_to(root).as_posix()] = digest.hexdigest()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["save", "check"])
    parser.add_argument("folder", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        if args.manifest.resolve().is_relative_to(args.folder.resolve()):
            raise ValueError("Keep the manifest outside the scanned folder")
        files = fingerprint(args.folder)
        if args.mode == "save":
            with args.manifest.open("x", encoding="utf-8") as out:
                json.dump(files, out, ensure_ascii=False, indent=2, sort_keys=True)
            print(f"Saved {len(files)} fingerprints.")
            return 0
        saved = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(saved, dict) or not all(isinstance(v, str) and len(v) == 64
                and all(c in "0123456789abcdef" for c in v) for v in saved.values()):
            raise ValueError("Invalid SHA-256 manifest")
        changes = { "added": sorted(files.keys() - saved.keys()),
                    "removed": sorted(saved.keys() - files.keys()),
                    "changed": sorted(k for k in files.keys() & saved.keys() if files[k] != saved[k]) }
        print(json.dumps(changes, indent=2, ensure_ascii=False))
        return int(any(changes.values()))
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())

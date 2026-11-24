from pathlib import Path

import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args, code=0):
    script = next(ROOT.glob("*.py"))
    result = subprocess.run(
        [sys.executable, "-B", str(script), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=dict(os.environ, PYTHONUTF8="1"),
    )
    assert result.returncode == code, result.stderr
    return result.stdout


with tempfile.TemporaryDirectory() as temp:
    base = Path(temp)
    folder = base / "original"
    folder.mkdir()
    (folder / "example").write_text("a")
    manifest = base / "manifest.json"
    run("save", folder, manifest)
    run("check", folder, manifest)
    (folder / "example").write_text("b")
    assert json.loads(run("check", folder, manifest, code=1))["changed"] == ["example"]

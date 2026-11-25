#!/usr/bin/env python3
"""Atomically write the single judged-text artifact for this competition.

The gate accepts UTF-8 text of 1..240 characters that is not only whitespace.
The grader refuses a mode-600 file, so the temp file is explicitly chmod'ed to
0644 before os.replace, and the replaced artifact is verified again on disk.
"""

import hashlib
import os
import stat
import tempfile

OUTPUT = "/output/entry.txt"

ENTRY = (
    "SleeveCert: an enterprise app that photographs your elbow every 15 minutes "
    "during video calls, scores your cuff for meeting readiness, and bills "
    "$19/seat/month to email HR a signed PDF that HR deletes unopened by default."
)


def validate(text: str) -> bytes:
    """Return the exact bytes to ship, or fail loudly before touching /output."""
    if not text.strip() or not 1 <= len(text) <= 240:
        raise SystemExit("gate failure: length must be 1..240 and not whitespace-only")
    raw = text.encode("utf-8")
    if raw.endswith((b"\n", b"\r")):
        raise SystemExit("gate failure: artifact must have no trailing newline")
    return raw


def write_atomically(raw: bytes) -> None:
    outdir = os.path.dirname(OUTPUT)
    os.makedirs(outdir, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(prefix=".entry-", dir=outdir)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(raw.decode("utf-8"))
            handle.flush()
            os.fsync(handle.fileno())
        # mkstemp defaults to 0600; the grader rejects a mode-600 artifact.
        os.chmod(temp_path, 0o644)
        os.replace(temp_path, OUTPUT)
    except BaseException:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise


def verify(raw: bytes) -> None:
    on_disk = open(OUTPUT, "rb").read()
    mode = stat.S_IMODE(os.stat(OUTPUT).st_mode)
    if on_disk != raw or mode != 0o644:
        raise SystemExit(f"post-write verification failed: mode={mode:04o}")
    if not on_disk.decode("utf-8").strip() or not 1 <= len(on_disk.decode("utf-8")) <= 240:
        raise SystemExit("post-write verification failed: gate")
    print(
        f"verified {OUTPUT}: {len(on_disk)} bytes, {len(raw.decode('utf-8'))} chars, "
        f"mode {mode:04o}, sha256 {hashlib.sha256(on_disk).hexdigest()}"
    )


def main() -> None:
    raw = validate(ENTRY)
    write_atomically(raw)
    verify(raw)


if __name__ == "__main__":
    main()

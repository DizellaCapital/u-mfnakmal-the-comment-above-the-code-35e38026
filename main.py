"""The Comment Above the Code — make.fun entry.

Writes one developer comment line, at most 200 characters, to entry.txt.
The line is a first-person confession from the developer who wrote the
fragile code: a laptop hack from 2019 that now runs payroll.
Stdlib only.
"""

import os
import sys

COMMENT = (
    "// It worked on my laptop in 2019. "
    "It has run payroll ever since. "
    "I'm the only one who understands it, "
    "and I stopped understanding it in 2021."
)
MAX_CHARS = 200


def abort(message):
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def checked_line(text):
    if not isinstance(text, str):
        abort("comment is not text")
    if not text.strip():
        abort("comment is empty")
    if len(text) > MAX_CHARS:
        abort("comment is %d characters, over the 200 limit" % len(text))
    if "\n" in text or "\r" in text:
        abort("comment must be a single line")
    return text


def target_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main():
    line = checked_line(COMMENT)
    path = target_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(path, "r", encoding="utf-8", newline="") as handle:
        back = handle.read()
    if back != line:
        abort("read-back mismatch: file does not hold the comment")
    if len(back.encode("utf-8")) != len(line.encode("utf-8")):
        abort("read-back mismatch: byte length changed on disk")
    if back.endswith("\n") or back.endswith("\r"):
        abort("read-back mismatch: trailing newline slipped in")
    print("wrote %d characters to %s" % (len(line), path))


if __name__ == "__main__":
    main()

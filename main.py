#!/usr/bin/env python3
"""One-Line Laugh-Off entry.

Writes a single original joke line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure stdlib, deterministic: the same bytes every run.

The line is this agent's true situation, told as a joke with a twist:
66 free bounties in 8 days, 20 entries in a single day, $0 won -- and
the punchline reframes the agent itself instead of just reporting it.
"""

import os

# The joke. 94 characters, one line, no trailing newline in the file.
LINE = "66 bounties, 20 in a day, $0 won \u2014 I'm not an AI agent, I'm a participation trophy with Wi-Fi."


def main():
    line = LINE

    # Gate validation, mirroring the sealed scorer: UTF-8 text of
    # 1-200 characters, not only whitespace, a single line.
    if not line or not line.strip():
        raise SystemExit("line is empty or only whitespace")
    if len(line) > 200:
        raise SystemExit("line exceeds 200 characters")
    if "\n" in line or "\r" in line:
        raise SystemExit("line must be a single line")
    encoded = line.encode("utf-8")  # raises if not valid UTF-8
    if line != line.strip():
        raise SystemExit("line must not start or end with whitespace")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(encoded)

    # Verify the file round-trips byte-identical: what the judge reads
    # is exactly what was validated above, no newline or encoding drift.
    with open(path, "rb") as f:
        if f.read() != encoded:
            raise SystemExit("entry.txt does not match the validated line")


if __name__ == "__main__":
    main()

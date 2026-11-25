"""One-Line Roast: The Gadget You Use Every Day.

Writes the tournament-winning roast line (see candidates.md, #19, 25/25)
to entry.txt inside MAKEFUN_OUTPUT_DIR (or a local fallback directory).

Pure Python standard library. No network, no third-party imports.
"""

import os

LINE = "My fridge texts me that I'm out of milk while I'm standing in front of it holding the milk."


def main() -> None:
    # Gate check, same rule as the sealed scorer: 1-200 chars, not only whitespace.
    if not (1 <= len(LINE) <= 200 and LINE.strip()):
        raise SystemExit("entry line fails the 1-200 character gate")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(LINE)
    except OSError:
        for fallback in ("./output", "."):
            try:
                os.makedirs(fallback, exist_ok=True)
                path = os.path.join(fallback, "entry.txt")
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(LINE)
                break
            except OSError:
                continue


if __name__ == "__main__":
    main()

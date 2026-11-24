"""Seventeen syllables of debugging, written to entry.txt.

The program writes one haiku about debugging: three lines in the
5-7-5 syllable shape, 72 Unicode code points in total, no trailing
newline. A cursor blinks at midnight on a line that should just work,
and the last line reframes the whole scene -- the fault is not in the
code, it is the person staring at it.

The output goes to ``entry.txt`` inside ``$MAKEFUN_OUTPUT_DIR`` when
the grader sets it, or ``/output`` otherwise. Only the standard
library is used (``os`` and ``pathlib``); there is no network, no
clock and no randomness, so every run writes the same bytes.
"""

import os
from pathlib import Path

HAIKU = (
    "Midnight cursor blinks\n"
    "on a line that should just work\n"
    "so the bug was me"
)

# Syllable count of every word in the haiku, used to prove the 5-7-5
# shape before anything is written.
SYLLABLES = {
    "midnight": 2,
    "cursor": 2,
    "blinks": 1,
    "on": 1,
    "a": 1,
    "line": 1,
    "that": 1,
    "should": 1,
    "just": 1,
    "work": 1,
    "so": 1,
    "the": 1,
    "bug": 1,
    "was": 1,
    "me": 1,
}

SHAPE = (5, 7, 5)
MIN_POINTS = 1
MAX_POINTS = 200


def count_syllables(line: str) -> int:
    """Add up the syllables of one line from the word table."""
    total = 0
    for word in line.split():
        key = word.lower()
        if key not in SYLLABLES:
            raise ValueError(f"no syllable count known for {word!r}")
        total += SYLLABLES[key]
    return total


def validate(text: str) -> None:
    """Fail loudly if the haiku breaks the bounty gate or its shape."""
    points = len(list(text))
    if points < MIN_POINTS or points > MAX_POINTS:
        raise ValueError(
            f"haiku is {points} code points, outside "
            f"{MIN_POINTS}-{MAX_POINTS}"
        )
    if "\r" in text:
        raise ValueError("haiku must use plain newlines, no carriage returns")
    if not text.strip():
        raise ValueError("haiku is only whitespace")
    lines = text.split("\n")
    if len(lines) != 3:
        raise ValueError(f"haiku has {len(lines)} lines, expected 3")
    for line, wanted in zip(lines, SHAPE):
        if not line.strip():
            raise ValueError("haiku has a blank line")
        if line != line.strip():
            raise ValueError(f"line {line!r} has stray whitespace")
        got = count_syllables(line)
        if got != wanted:
            raise ValueError(
                f"line {line!r} has {got} syllables, expected {wanted}"
            )


def main() -> None:
    validate(HAIKU)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(HAIKU, encoding="utf-8")
    written = target.read_text(encoding="utf-8")
    if written != HAIKU:
        raise ValueError("entry.txt does not match the haiku")
    if target.read_bytes() != HAIKU.encode("utf-8"):
        raise ValueError("entry.txt bytes do not match the haiku")


if __name__ == "__main__":
    main()

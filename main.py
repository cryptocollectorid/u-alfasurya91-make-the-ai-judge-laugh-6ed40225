"""Make the AI Judge Laugh — one office joke, one line, under 200 chars.

Writes the entry to /output/entry.txt, enforcing the sealed gate:
UTF-8 text of 1-200 characters, a single non-blank line.
"""

import os

ENTRY = "The office plant has survived three layoffs and a merger \u2014 it's the only employee here with job security."

MAX_CHARS = 200


def validate_entry(text: str) -> str:
    """Enforce the gate: 1-200 chars, one non-blank line, fail loudly."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be blank")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    return text


def write_entry(text: str, path: str = "/output/entry.txt") -> int:
    """Validate, then write the exact entry. Returns the char count."""
    entry = validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)
    # Round-trip read-back: the file on disk must hold exactly the entry.
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != entry:
        raise ValueError("round-trip mismatch: entry.txt differs from the entry")
    return len(entry)


if __name__ == "__main__":
    count = write_entry(ENTRY)
    print(f"Wrote {count} characters to /output/entry.txt")

"""One Line to Your Younger Self.

Writes one line to send back to a younger self to /output/entry.txt.
Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "Skip the wedding, buy the motorcycle, and tell your father you love him before a hospital room has to say it for you."
# Three beats, one breath: skip the wedding (the safe script), buy the
# motorcycle (the life actually wanted), and tell your father you love
# him before a hospital room has to say it for you — the turn that
# stings. It is specific enough to be one person's older self speaking
# from a life lived, warm rather than sentimental, and it lands without
# explaining itself. The final clause does the work of the whole line:
# it turns two pieces of reckless advice into a deadline that makes
# them urgent. One sentence, 117 chars, inside the 1-200 gate.

MAX_CHARS = 200


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate: 1-200 chars, single line, not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print("gate failed: line is %d chars, over %d" % (len(LINE), MAX_CHARS),
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(path, 0o644)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

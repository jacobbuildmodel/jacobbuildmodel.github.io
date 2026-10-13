#!/usr/bin/env python3
"""
guard_open_pages.py -- a Claude Code PreToolUse hook that refuses an Edit,
MultiEdit or Write that would change the body of a sealed open question page.

Registered in .claude/settings.json (matcher Edit|MultiEdit|Write). Reads the
hook JSON on stdin. Standard library only.

A page is sealed when content/open/<page>.md has an entry in
data/open_seals.yaml. The hook builds the file as it would be after the edit,
computes its body md5 with check_open_pages.py's own split_front_matter, and
exits 2 (the edit is refused, the reason goes back to Claude) if that md5
differs from the entry's body_md5. Front-matter-only edits, such as the
answered: marker, leave the body alone and pass. Any other path passes.

The repo root is found from the edited file itself (the nearest parent with
data/open_seals.yaml), so the guard also covers fresh clones elsewhere on disk.
Line endings are compared as LF, the way git stores them: under Windows
core.autocrlf a working copy is CRLF, and its committed blob is what the
sealed md5 was taken from.

On any error inside the hook it fails open: a warning on stderr, exit 0, so a
bug here never blocks unrelated work. CI (open-pages.yml) is still the backstop.
Edits made through Bash (sed, a script) are not seen by this hook.

To remove: delete the PreToolUse entry from .claude/settings.json.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_open_pages import parse_seals, split_front_matter  # noqa: E402

SEALS = Path("data/open_seals.yaml")
TOOLS = ("Edit", "MultiEdit", "Write")
ADVICE = ("edit the front matter only, or add a reason: line in "
          "data/open_seals.yaml in a PR Jacob approves")


def lf(text):
    return text.replace("\r\n", "\n")


def find_root(target):
    for parent in target.parents:
        if (parent / SEALS).is_file():
            return parent
    return None


def apply_edit(text, old, new, replace_all):
    """Return the text after one Edit step, or None if old_string is not
    there (the tool itself will then refuse the edit)."""
    old, new = lf(old), lf(new)
    if not old or old not in text:
        return None
    return text.replace(old, new) if replace_all else text.replace(old, new, 1)


def after_edit(tool, tool_input, target):
    """The file's text, LF, as it would be after the tool call; None if the
    edit cannot apply."""
    if tool == "Write":
        return lf(tool_input.get("content", ""))
    text = lf(target.read_bytes().decode("utf-8"))
    if tool == "Edit":
        steps = [tool_input]
    else:
        steps = tool_input.get("edits") or []
    for step in steps:
        text = apply_edit(text, step.get("old_string", ""),
                          step.get("new_string", ""),
                          bool(step.get("replace_all")))
        if text is None:
            return None
    return text


def check(event):
    """Return the one-line refusal, or None to let the tool call through."""
    tool = event.get("tool_name")
    if tool not in TOOLS:
        return None
    tool_input = event.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return None
    target = Path(file_path)
    if not target.is_absolute():
        target = Path(event.get("cwd") or ".") / target
    target = target.resolve()
    root = find_root(target)
    if root is None:
        return None
    rel = target.relative_to(root).as_posix()
    seals, errors = parse_seals((root / SEALS).read_text(encoding="utf-8"),
                                str(SEALS))
    if errors:
        raise ValueError("; ".join(errors))
    entry = seals.get(rel)
    if entry is None:
        return None
    if tool != "Write" and not target.is_file():
        return None
    text = after_edit(tool, tool_input, target)
    if text is None:
        return None
    front, body = split_front_matter(text.encode("utf-8"))
    got = hashlib.md5(body).hexdigest() if front is not None else "no front matter"
    if got == entry.get("body_md5"):
        return None
    return (f"seal guard: {rel} is sealed by {entry.get('seal')} and this "
            f"edit changes its body (md5 {got} != {entry.get('body_md5')}): "
            f"{ADVICE}")


def main():
    try:
        refusal = check(json.loads(sys.stdin.read() or "{}"))
    except Exception as exc:  # fail open: a hook bug must not block work
        print(f"seal guard: warning, hook error, edit allowed: {exc!r}",
              file=sys.stderr)
        return 0
    if refusal:
        print(refusal, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

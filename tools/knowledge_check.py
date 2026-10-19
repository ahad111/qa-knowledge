#!/usr/bin/env python3
"""Knowledge PR check: fails on copied code, secrets or disallowed file types in changed files."""
import re, subprocess, sys
from pathlib import Path

ALLOWED_EXT = {".md", ".yaml", ".yml", ".json"}
ALLOWED_FENCES = {"mermaid", "yaml", "yml", "json", ""}
MAX_EXAMPLE_LINES = 15
SECRETS = [r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*\S{8,}",
           r"ghp_[A-Za-z0-9]{30,}", r"xox[bap]-[A-Za-z0-9-]{10,}"]

def changed_files(base):
    out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"], capture_output=True, text=True, check=True).stdout
    return [f for f in out.split() if f and not f.startswith(".github/") and not f.startswith("tools/")]

def check(path):
    errors, p = [], Path(path)
    if p.suffix.lower() not in ALLOWED_EXT and p.name != "CODEOWNERS":
        return [f"{path}: file type {p.suffix or '(none)'} not allowed in knowledge"]
    text = p.read_text(errors="ignore")
    for pat in SECRETS:
        if re.search(pat, text):
            errors.append(f"{path}: looks like a secret ({pat})")
    for m in re.finditer(r"```([A-Za-z0-9_+-]*)\n(.*?)```", text, re.S):
        lang, body = m.group(1).lower(), m.group(2)
        if lang not in ALLOWED_FENCES:
            errors.append(f"{path}: code block in '{lang}' — knowledge holds descriptions and pointers, never code")
        elif lang in {"yaml", "yml", "json", ""} and body.count("\n") > MAX_EXAMPLE_LINES:
            errors.append(f"{path}: example block longer than {MAX_EXAMPLE_LINES} lines")
    return errors

if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    errs = [e for f in changed_files(base) if Path(f).exists() for e in check(f)]
    print("\n".join(errs) or "OK — knowledge check passed")
    sys.exit(1 if errs else 0)

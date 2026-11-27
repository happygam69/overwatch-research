#!/usr/bin/env python3
"""One-off: move the ledger-94 line from inside the synthesis list to the
corrections ledger (right after ledger 93). Pass-76 CODE_MAP fixup."""
import re, sys

path = "/home/z/my-project/overwatch-research/CODE_MAP.md"
lines = open(path, encoding="utf-8").read().split("\n")

# locate the misplaced ledger 94 line (starts with '94. **Pass 76')
idx94 = next(i for i, l in enumerate(lines) if l.startswith("94. **Pass 76"))
ledger94 = lines.pop(idx94)

# locate ledger 93 (corrections section) and insert after it
idx93 = next(i for i, l in enumerate(lines) if l.startswith("93. **Pass 75"))
lines.insert(idx93 + 1, ledger94)

open(path, "w", encoding="utf-8").write("\n".join(lines))
print(f"moved ledger 94 from line {idx94+1} to after ledger 93 (line {idx93+2}); total lines {len(lines)}")

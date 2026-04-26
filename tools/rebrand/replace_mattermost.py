#!/usr/bin/env python3
"""Rebrand standalone "Mattermost" -> "BizerOS Chat" in user-facing files.

Case-sensitive. Preserves compound forms like "Mattermost, Inc.",
"Mattermost Cloud", "Mattermost Server", etc. via negative lookahead.
"""

from __future__ import annotations

import glob
import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

PRESERVE = (
    r"(?:,?\s*(?:Inc\.|Cloud|Server|Enterprise|Professional|Free|Starter|"
    r"Edition|Cluster|Agents|AI|Boards|Playbooks|Calls|Mobile|Desktop|"
    r"Apps|Bot|API))"
)
PATTERN = re.compile(r"\bMattermost\b(?!" + PRESERVE + r")")
REPLACEMENT = "BizerOS Chat"


def collect_targets() -> list[str]:
    targets: list[str] = []
    targets += sorted(glob.glob(os.path.join(REPO, "webapp/channels/src/i18n/*.json")))
    targets += sorted(glob.glob(os.path.join(REPO, "server/i18n/*.json")))
    targets += [
        os.path.join(REPO, "server/templates/globalrelay_compliance_export.html"),
        os.path.join(REPO, "server/templates/unsupported_desktop_app.html"),
        os.path.join(REPO, "server/public/model/config.go"),
        os.path.join(REPO, "server/channels/app/email/service.go"),
        os.path.join(REPO, "webapp/channels/src/root.html"),
        os.path.join(REPO, "webapp/channels/webpack.config.js"),
        os.path.join(
            REPO,
            "webapp/channels/src/components/global_header/left_controls/"
            "product_menu/product_menu_list/index.ts",
        ),
        os.path.join(
            REPO, "webapp/channels/src/components/header_footer_route/header.tsx"
        ),
        os.path.join(
            REPO,
            "webapp/channels/src/components/admin_console/admin_definition.tsx",
        ),
    ]
    return targets


def replace_in_file(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        original = f.read()
    new, count = PATTERN.subn(REPLACEMENT, original)
    if count:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return count


def main() -> int:
    targets = collect_targets()
    missing = [p for p in targets if not os.path.exists(p)]
    if missing:
        print("ERROR: missing target files:", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        return 1

    total = 0
    files_changed = 0
    for path in targets:
        n = replace_in_file(path)
        if n:
            files_changed += 1
            total += n
            rel = os.path.relpath(path, REPO)
            print(f"{n:>4}  {rel}")
    print(f"\nReplaced {total} occurrences across {files_changed} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

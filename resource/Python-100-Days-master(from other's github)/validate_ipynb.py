#!/usr/bin/env python3
"""Validate generated notebooks and syntax-check their Python cells."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from convert_md_to_ipynb import syntax_check_source


def main() -> None:
    root = Path(__file__).resolve().parent / "ipynb版笔记"
    notebooks = sorted(root.rglob("*.ipynb"))
    failures: list[tuple[Path, int, str, str]] = []
    code_cells = 0
    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        assert isinstance(notebook["cells"], list)
        for index, cell in enumerate(notebook["cells"], 1):
            if cell["cell_type"] != "code":
                continue
            code_cells += 1
            source = "".join(cell["source"])
            try:
                ast.parse(syntax_check_source(source), filename=f"{path}#cell-{index}")
            except SyntaxError as error:
                failures.append((path, index, str(error), source))

    print(f"Validated {len(notebooks)} notebooks and {code_cells} code cells")
    if failures:
        print(f"Syntax failures: {len(failures)}")
        for path, index, error, source in failures:
            print(f"{path.relative_to(root)} | cell {index} | {error}")
            print(repr(source[:500]))
        raise SystemExit(1)
    print("All Python code cells passed syntax validation")


if __name__ == "__main__":
    main()

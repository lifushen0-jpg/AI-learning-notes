#!/usr/bin/env python3
"""Convert every Markdown note in this repository into a Jupyter notebook.

Python fenced blocks become executable code cells.  All prose and fenced blocks
in other languages remain in Markdown cells.  The output tree mirrors the input
tree beneath ``ipynb版笔记``.
"""

from __future__ import annotations

import argparse
import doctest
import hashlib
import json
import re
import textwrap
from pathlib import Path


PYTHON_LANGUAGES = {"python", "py", "python3"}
FENCE_RE = re.compile(r"^(?P<indent> {0,3})(?P<fence>`{3,}|~{3,})(?P<info>.*)$")


def source_lines(text: str) -> list[str]:
    """Return notebook-style source lines while preserving final newlines."""
    return text.splitlines(keepends=True)


def flush_markdown(cells: list[dict], lines: list[str]) -> None:
    """Append a non-empty Markdown cell, trimming only excess blank edges."""
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if lines:
        if not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        cells.append({"cell_type": "markdown", "metadata": {}, "source": lines.copy()})
    lines.clear()


def syntax_check_source(source: str) -> str:
    """Replace IPython line magics with ``pass`` for a standard Python parse."""
    checked: list[str] = []
    for line in source.splitlines(keepends=True):
        if line.lstrip().startswith(("%", "!")):
            indent = line[: len(line) - len(line.lstrip())]
            newline = "\n" if line.endswith("\n") else ""
            checked.append(f"{indent}pass  # IPython command{newline}")
        else:
            checked.append(line)
    return "".join(checked)


def make_runnable(source: str) -> tuple[str, bool]:
    """Normalize common tutorial snippets and guarantee parseable code cells.

    Returns the normalized source and whether an incomplete/non-Python snippet
    had to be retained as comments.
    """
    source = source.expandtabs(4).replace("\u00a0", " ")

    # Convert copied interpreter sessions to a script; expected results become
    # comments, so the original teaching context remains visible.
    if any(line.lstrip().startswith(">>>") for line in source.splitlines()):
        source = doctest.script_from_examples(source)

    lines = source.splitlines(keepends=True)
    normalized: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == "...":
            indent = line[: len(line) - len(line.lstrip())]
            normalized.append(f"{indent}# ...\n")
        elif stripped.startswith("pip install "):
            indent = line[: len(line) - len(line.lstrip())]
            normalized.append(f"{indent}%{line.lstrip()}")
        elif stripped.startswith("python3 -m "):
            indent = line[: len(line) - len(line.lstrip())]
            normalized.append(f"{indent}!python -m {line.lstrip()[11:]}")
        else:
            normalized.append(line)
    source = "".join(normalized)

    try:
        compile(syntax_check_source(source), "<notebook-cell>", "exec")
        return source, False
    except SyntaxError:
        # Some source notes intentionally show partial statements, command
        # output, or abbreviated framework configuration.  Keep every original
        # line visible while making the cell safe to run as a no-op.
        commented = "# 原笔记中的示例不完整或包含非 Python 输出，保留如下：\n"
        commented += "".join(
            f"# {line}" if line.strip() else "#\n"
            for line in source.splitlines(keepends=True)
        )
        if commented and not commented.endswith("\n"):
            commented += "\n"
        return commented, True


def markdown_to_cells(text: str) -> list[dict]:
    """Split Markdown at Python fences without disturbing other fences."""
    cells: list[dict] = []
    markdown: list[str] = []
    lines = text.splitlines(keepends=True)
    index = 0

    while index < len(lines):
        opening = FENCE_RE.match(lines[index].rstrip("\r\n"))
        if not opening:
            markdown.append(lines[index])
            index += 1
            continue

        fence = opening.group("fence")
        fence_char = fence[0]
        fence_length = len(fence)
        info = opening.group("info").strip()
        language = info.split(maxsplit=1)[0].lower() if info else ""

        closing_index = index + 1
        while closing_index < len(lines):
            possible_close = FENCE_RE.match(lines[closing_index].rstrip("\r\n"))
            if (
                possible_close
                and possible_close.group("fence")[0] == fence_char
                and len(possible_close.group("fence")) >= fence_length
                and not possible_close.group("info").strip()
            ):
                break
            closing_index += 1

        # An unmatched fence is ordinary Markdown.
        if closing_index == len(lines):
            markdown.extend(lines[index:])
            break

        if language in PYTHON_LANGUAGES:
            flush_markdown(cells, markdown)
            # Markdown permits fenced blocks to be indented inside list items.
            # Remove that common structural indentation before making a cell.
            code_text = textwrap.dedent("".join(lines[index + 1 : closing_index]))
            code_text, is_fragment = make_runnable(code_text)
            code = code_text.splitlines(keepends=True)
            while code and not code[0].strip():
                code.pop(0)
            while code and not code[-1].strip():
                code.pop()
            if code:
                if not code[-1].endswith("\n"):
                    code[-1] += "\n"
                cells.append(
                    {
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {"tags": ["source-fragment"]} if is_fragment else {},
                        "outputs": [],
                        "source": code,
                    }
                )
        else:
            markdown.extend(lines[index : closing_index + 1])

        index = closing_index + 1

    flush_markdown(cells, markdown)
    return cells


def notebook_for(markdown: str) -> dict:
    return {
        "cells": markdown_to_cells(markdown),
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def convert_tree(root: Path, output: Path) -> tuple[int, int]:
    markdown_files = sorted(
        path for path in root.rglob("*.md") if output not in path.parents
    )
    code_cells = 0
    for source in markdown_files:
        relative = source.relative_to(root)
        destination = output / relative.with_suffix(".ipynb")
        destination.parent.mkdir(parents=True, exist_ok=True)
        notebook = notebook_for(source.read_text(encoding="utf-8-sig"))
        for index, cell in enumerate(notebook["cells"]):
            identity = f"{relative.as_posix()}:{index}".encode("utf-8")
            cell["id"] = hashlib.sha1(identity).hexdigest()[:12]
        code_cells += sum(cell["cell_type"] == "code" for cell in notebook["cells"])
        destination.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
    return len(markdown_files), code_cells


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or root / "ipynb版笔记").resolve()
    count, code_cells = convert_tree(root, output)
    print(f"Converted {count} Markdown files with {code_cells} Python code cells to {output}")


if __name__ == "__main__":
    main()

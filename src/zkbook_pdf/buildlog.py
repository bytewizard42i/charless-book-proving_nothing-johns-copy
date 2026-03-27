"""Shared logging helpers for PDF build workflows."""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class BuildLog:
    """Collect log lines and mirror them to stdout and an optional file."""

    path: Path | None = None
    lines: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("", encoding="utf-8")

    def _emit(self, line: str) -> None:
        encoding = sys.stdout.encoding or "utf-8"
        safe_line = line.encode(encoding, errors="replace").decode(
            encoding,
            errors="replace",
        )
        print(safe_line)
        self.lines.append(line)
        if self.path is not None:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def section(self, name: str) -> None:
        self._emit(f"[{name}]")

    def info(self, message: str) -> None:
        self._emit(f"INFO: {message}")

    def warn(self, message: str) -> None:
        self._emit(f"WARNING: {message}")

    def error(self, message: str) -> None:
        self._emit(f"ERROR: {message}")

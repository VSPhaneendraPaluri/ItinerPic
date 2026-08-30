"""File I/O utilities."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def write_file(
    path: Path,
    content: str,
    encoding: str = "utf-8",
    overwrite: bool = True,
    backup: bool = False,
) -> None:
    """
    Write content to file safely.

    Args:
        path: File path to write to
        content: Content to write
        encoding: File encoding
        overwrite: Whether to overwrite existing file
        backup: Create backup if file exists

    Raises:
        FileExistsError: If file exists and overwrite is False
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {path}")

    if path.exists() and backup:
        backup_path = path.with_suffix(path.suffix + ".bak")
        path.rename(backup_path)
        logger.info(f"Backed up existing file to {backup_path}")

    path.write_text(content, encoding=encoding)
    logger.info(f"Wrote {len(content)} bytes to {path}")


def read_file(
    path: Path,
    encoding: str = "utf-8",
) -> str:
    """
    Read file content.

    Args:
        path: File path to read
        encoding: File encoding

    Returns:
        File content

    Raises:
        FileNotFoundError: If file does not exist
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    content = path.read_text(encoding=encoding)
    logger.debug(f"Read {len(content)} bytes from {path}")
    return content

from pathlib import Path

from functions.common import resolve_within
from functions.errors import NotAFileError, PathTraversalError

MAX_CHARS = 10_000


def get_file_content(working_dir: str, file_path: str) -> str:
    try:
        target = resolve_within(working_dir, file_path, "read")
        if not target.is_file():
            raise NotAFileError(f"File not found or is not a regular file: {file_path}")
        return read_file(target, file_path)
    except (PathTraversalError, OSError, ValueError) as e:
        return f"Error: {e}"


def read_file(target: Path, display_path: str, chars: int = MAX_CHARS) -> str:
    with open(target, "r", encoding="utf-8") as f:
        content = f.read(chars)
        if f.read(1):
            content += f'[...File "{display_path}" truncated at {chars} characters]'
        return content

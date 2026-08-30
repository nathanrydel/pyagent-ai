import os
from pathlib import Path

from functions.common import resolve_within
from functions.errors import PathTraversalError


def get_files_info(working_dir: str, dir: str) -> str:
    try:
        target = resolve_within(working_dir, dir, "list")
        if not target.is_dir():
            raise NotADirectoryError(f'"{dir}" is not a directory')
        return format_directory_content(target)
    except (PathTraversalError, OSError) as e:
        return f"Error: {e}"


def format_directory_content(path: Path) -> str:
    lines = []
    with os.scandir(path) as entries:
        for entry in sorted(entries, key=lambda e: e.name):
            lines.append(
                f"- {entry.name}: file_size={entry.stat().st_size} bytes, "
                f"is_dir={entry.is_dir()}"
            )
    return "\n".join(lines)


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

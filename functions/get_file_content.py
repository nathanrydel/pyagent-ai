from pathlib import Path

from functions.common import resolve_within
from functions.errors import NotAFileError, PathTraversalError

MAX_CHARS = 10_000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target = resolve_within(working_directory, file_path, "read")
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


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": (
            "Reads and returns the contents of a file relative to the working "
            "directory, truncated if the file is very large"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

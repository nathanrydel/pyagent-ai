from functions.common import resolve_within
from functions.errors import PathTraversalError


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        target = resolve_within(working_directory, file_path, "write to")
        if target.is_dir():
            raise IsADirectoryError(
                f'Cannot write to "{file_path}" as it is a directory'
            )
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except (PathTraversalError, OSError, ValueError) as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": (
            "Writes content to a file relative to the working directory, "
            "creating it (and any parent directories) if it doesn't exist, or "
            "overwriting it if it does"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

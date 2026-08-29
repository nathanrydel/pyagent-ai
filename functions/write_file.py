from functions.common import resolve_within
from functions.errors import PathTraversalError


def write_file(working_dir: str, file_path: str, content: str) -> str:
    try:
        target = resolve_within(working_dir, file_path, "write to")
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

from pathlib import Path

from functions.errors import PathTraversalError


def resolve_within(working_dir: str, rel_path: str, verb: str) -> Path:
    base = Path(working_dir).resolve()
    target = (base / rel_path).resolve()
    if not target.is_relative_to(base):
        raise PathTraversalError(
            f'Cannot {verb} "{rel_path}" as it is outside the permitted working directory'
        )
    return target

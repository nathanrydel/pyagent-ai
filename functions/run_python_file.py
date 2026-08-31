import subprocess
from pathlib import Path

from functions.common import resolve_within
from functions.errors import NotAFileError, NotAPythonFileError, PathTraversalError

TIMEOUT_SECONDS = 30


def run_python_file(
    working_dir: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        base = Path(working_dir).resolve()
        target = resolve_within(working_dir, file_path, "execute")
        if not target.is_file():
            raise NotAFileError(
                f'"{file_path}" does not exist or is not a regular file'
            )
        if target.suffix != ".py":
            raise NotAPythonFileError(f'"{file_path}" is not a Python file')

        command = ["python", str(target)]
        if args:
            command.extend(args)

        completed = subprocess.run(
            command,
            cwd=base,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        return format_result(completed)
    except (PathTraversalError, NotAFileError, NotAPythonFileError) as e:
        return f"Error: {e}"
    except (OSError, ValueError, subprocess.SubprocessError) as e:
        return f"Error: executing Python file: {e}"


def format_result(completed: subprocess.CompletedProcess) -> str:
    parts = []
    if completed.stdout:
        parts.append(f"STDOUT:\n{completed.stdout}")
    if completed.stderr:
        parts.append(f"STDERR:\n{completed.stderr}")
    if not parts:
        parts.append("No output produced")
    if completed.returncode != 0:
        parts.append(f"Process exited with code {completed.returncode}")
    return "\n".join(parts)


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": (
            "Executes a Python file relative to the working directory with an "
            "optional list of command-line arguments, and returns its stdout, "
            "stderr, and exit code"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python file",
                },
            },
            "required": ["file_path"],
        },
    },
}

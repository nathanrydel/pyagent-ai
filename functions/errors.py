class NotAFileError(OSError):
    """Requested path is not a regular file"""


class NotAPythonFileError(Exception):
    """Requested path is not a .py file"""


class PathTraversalError(Exception):
    """Requested path escapes the permitted working directory."""

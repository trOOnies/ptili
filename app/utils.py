"""Utils script."""

import os
import re

# Regular expression for reserved names (Windows specific)
RESERVED_PATT = re.compile(r"^(con|prn|aux|nul|com[1-9]|lpt[1-9])$", re.IGNORECASE)


def path_is_safe(path: str) -> bool:
    """Check if the provided path is safe."""
    if not isinstance(path, str) or not path:
        return False

    unsafe_elements = ["..", "$", "\\", ":", "*", "?", '"', "'", "<", ">", "|"]
    if any(e in path for e in unsafe_elements):
        return False

    if os.path.isabs(path):
        return False

    # Split the path into components and check for reserved names
    path_components = os.path.split(path)
    for component in path_components:
        if RESERVED_PATT.match(component):
            return False

    return True

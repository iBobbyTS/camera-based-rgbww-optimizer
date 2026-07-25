"""Shared positive context for local-lab control command help."""

LOCAL_LAB_CONTEXT = "For a user-owned local photography and lighting calibration lab."


def cli_description(action: str) -> str:
    """Combine a concise command action with the shared local-lab context."""

    return f"{action.rstrip()} {LOCAL_LAB_CONTEXT}"

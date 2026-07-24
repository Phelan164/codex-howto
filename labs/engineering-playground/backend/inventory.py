"""Small inventory domain used by the Codex How To engineering lab."""


def reserve(available: int, quantity: int) -> int:
    """Return remaining stock after reserving quantity.

    A reservation must use positive whole numbers and cannot exceed stock.
    """
    if quantity > available:
        raise ValueError("insufficient stock")
    return available - quantity

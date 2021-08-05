"""File with only sanitizeStr function."""

def sanitizeStr(data):
    """
    Escape all char that will trigger an error.

    Parameters
    ----------
    data: str
        the str to sanitize

    Returns
    -------
    str
        The sanitized data.
    """
    data = " ".join(data.split())
    new_msg = []
    for letter in data:
        if letter in ['"',"\\"]:
            new_msg.append("\\")
        new_msg.append(letter)
    return "".join(new_msg)
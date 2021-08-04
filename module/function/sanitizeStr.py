"""
file with only sanitizeStr function
"""

def sanitizeStr(data):
    """
    goal :
        escape all char that will trigger an error
    arg :
        data : the str to sanitize
    return :
        the sanitize data
    """
    data = " ".join(data.split())
    new_msg = []
    for letter in data:
        if letter in ['"',"\\"]:
            new_msg.append("\\")
        new_msg.append(letter)
    return "".join(new_msg)
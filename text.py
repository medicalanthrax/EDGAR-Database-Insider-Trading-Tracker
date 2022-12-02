"""Contains the text() method"""
def text(field):
    """Prevent noneType errors when calling .text on objects in read_data."""
    if field is not None:
        return field.text
    return "N/A"

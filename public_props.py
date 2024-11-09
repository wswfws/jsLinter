"""
Module containing utility functions for object property inspection.

Functions:
- get_public_props: Retrieve a list of public properties of an object (excluding private and protected properties).

Usage:
from public_props import get_public_props

# Example usage
class Example:
    def __init__(self):
        self.public_prop = "I am public"
        self._private_prop = "I am private"

example = Example()
public_properties = get_public_props(example)
print(public_properties)  # Output: ['public_prop']
"""

def get_public_props(obj):
    """
    Retrieves a list of public properties for a given object.

    Args:
        obj: The object whose properties are to be inspected.

    Returns:
        list[str]: A list containing the names of public properties (those that do not start with an underscore).

    Example:
        >>> class Sample:
        ...     def __init__(self):
        ...         self.public_attr = 1
        ...         self._private_attr = 2
        >>> sample = Sample()
        >>> get_public_props(sample)
        ['public_attr']
    """
    return [name for name in dir(obj) if not name.startswith('_')]

"""
Module containing classes for working with JavaScript code analysis.

Classes:
- JsCode: Data class to represent JavaScript code and perform analysis.
- JsCodeError: Custom exception class for JavaScript code errors.
- JsCodeWarning: Custom warning class for JavaScript code warnings.
"""
from dataclasses import dataclass

import esprima


@dataclass
class JsCode:
    """
    Data class to represent JavaScript code and perform analysis.

    Attributes:
        code: The JavaScript code.
        line_code: List of code lines.
        errors: List to store errors found during analysis.
        parsed_code: Parsed code using esprima library.
        tokenize_code: Tokenize code using esprima library.
        filename: Name of the file associated with the code.
    """

    code: str
    filename: str = "no_filename"

    def __post_init__(self):
        self.line_code = self.code.split("\n")
        self.errors = []
        self.parsed_code = esprima.parseScript(self.code, tolerant=True, loc=True)
        self.tokenize_code = esprima.tokenize(self.code, tolerant=True, loc=True)


class JsCodeError(Exception):
    """
    Custom exception class for JavaScript code errors.

    Attributes:
       message (str): Error message.
       filename (str): Name of the file where the error occurred.
       lineno (int): Line number where the error occurred.

    Methods:
       __init__: Initializes JsCodeError object.
       __str__: String representation of the exception.
    """

    def __init__(self, message, filename, lineno):
        self.message = message
        self.filename = filename
        self.lineno = lineno

    def __str__(self):
        return f'Error: {self.filename} line {self.lineno}: {self.message}'


class JsCodeWarning(Warning):
    """
    Custom warning class for JavaScript code warnings.

    Attributes:
        message (str): Warning message.
        filename (str): Name of the file where the warning occurred.
        lineno (int): Line number where the warning occurred.

    Methods:
        __init__: Initializes JsCodeWarning object.
        __str__: String representation of the warning.
    """

    def __init__(self, message, filename, lineno):
        self.message = message
        self.filename = filename
        self.lineno = lineno

    def __str__(self):
        return f'Warning: {self.filename} line {self.lineno}: {self.message}'

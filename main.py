"""
Тут всё будет переписано
"""

import esprima
from yaml import load as load_yaml, FullLoader

from checkers.correct_naming import check_for_correct_naming
from checkers.empty_lines import check_for_empty_lines
from checkers.missing_semicolons import check_for_missing_semicolons
from checkers.spaces_style import check_spaces_style
from config import CONFIG_PATH, CONFIG_ENCODING
from self_types.js_code import JsCode, JsCodeError, JsCodeWarning


class SimpleJSLinter:
    """
    Class for linting JavaScript code and reporting errors and warnings.

    Attributes:
        js_code (JsCode): The JavaScript code object to be linted.
        errors (list[JsCodeError]): List to store linting errors.
        warnings (list[JsCodeWarning]): List to store linting warnings.
    """

    def __init__(self, js_code: JsCode):
        self.js_code = js_code
        self.errors: list[JsCodeError] = []
        self.warnings: list[JsCodeWarning] = []

    def lint(self, **kwargs):
        """
        Lints the JavaScript code for errors.

        Args:
            **kwargs: Keyword arguments to specify which specific checks to run.
                      Pass 'missing_semicolons=True' to check for missing semicolons.
                      Pass 'empty_lines=True' to checking empty lines.
                      Pass 'all=True' to run all available checks.
        """

        checkers = kwargs.get('checkers', {})

        try:
            check_all = checkers.get("all", False)
            if check_all or checkers.get("missing_semicolons"):
                self.warnings.extend(check_for_missing_semicolons(self.js_code))
            if check_all or checkers.get("empty_lines"):
                self.warnings.extend(check_for_empty_lines(
                    self.js_code,
                    kwargs.get("max-code-line-without-empty-lines", 9)
                ))
            if check_all or checkers.get("spaces_style"):
                self.warnings.extend(check_spaces_style(
                    self.js_code,
                    kwargs.get("spaces-style", {})
                ))
            if check_all or checkers.get("correct_naming"):
                self.warnings.extend(check_for_correct_naming(self.js_code))
        except esprima.Error as e:
            print(f"Parsing error: {e.message}")

    def report(self):
        """Reports the linting errors and warnings found in the JavaScript code."""
        if not self.errors and not self.warnings:
            print("No linting errors found!")
        else:
            for error in self.errors:
                print(error)
            for warning in self.warnings:
                print(warning)




with open(CONFIG_PATH, 'r', encoding=CONFIG_ENCODING) as f:
    config = load_yaml(f, Loader=FullLoader)

with open("test1.js", 'r', encoding=CONFIG_ENCODING) as f:
    code1 = JsCode(f.read())

linter = SimpleJSLinter(code1)
linter.lint(**config)
linter.report()

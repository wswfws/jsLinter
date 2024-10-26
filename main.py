"""
Тут всё будет переписано
"""

import esprima
from yaml import load as load_yaml, FullLoader

from checkers.empty_lines import check_for_empty_lines
from checkers.missing_semicolons import check_for_missing_semicolons
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
                    kwargs.get("max_code_lines_without_empty_line", 9)
                ))
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


# Пример использования:
SIMPLE_CODE = """
let a = 5
console.log(a)
"""

with open(CONFIG_PATH, 'r', encoding=CONFIG_ENCODING) as f:
    config = load_yaml(f, Loader=FullLoader)

code1 = JsCode(SIMPLE_CODE)

linter = SimpleJSLinter(code1)
linter.lint(**config)
linter.report()

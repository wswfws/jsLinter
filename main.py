"""
Тут всё будет переписано
"""

import esprima

from checkers.missing_semicolons import check_for_missing_semicolons
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
                      Pass 'all=True' to run all available checks.
        """

        try:
            check_all = kwargs.get("all", False)
            if check_all or kwargs.get("missing_semicolons"):
                self.warnings.extend(check_for_missing_semicolons(self.js_code))
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

# with open("test1.js", "r") as f:
#     simple_code = f.read()

code1 = JsCode(SIMPLE_CODE)

linter = SimpleJSLinter(code1)
linter.lint(all=True)
linter.report()

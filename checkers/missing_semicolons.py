"""
Module containing functions for JavaScript linting.

Functions:
- check_for_missing_semicolons: Checks for missing semicolons in the JavaScript code.

Usage:
from self_types.js_code import JsCode, JsCodeWarning

# Example usage
code = JsCode("let a = 5")
warnings = check_for_missing_semicolons(code)
for warning in warnings:
    print(warning)
"""
from self_types.js_code import JsCode, JsCodeWarning


def check_for_missing_semicolons(js_code: JsCode) -> list[JsCodeWarning]:
    """
    Check for missing semicolons at the end of statements in the JavaScript code.

    Args:
        js_code (JsCode): The JsCode object representing the JavaScript code.

    Returns:
        list[JsCodeWarning]: A list of JsCodeWarning objects representing missing semicolons warnings.
    """

    def check(body):
        for node in body:
            if node.type == "FunctionDeclaration":
                check(node.body.body)
                continue
            last_symbol = js_code.line_code[node.loc.end.line - 1][node.loc.end.column - 1]
            if last_symbol != ";":
                errors.append(JsCodeWarning("Missing semicolon", js_code.filename, node.loc.start.line))

    errors: list[JsCodeWarning] = []
    check(js_code.parsed_code.body)
    return errors

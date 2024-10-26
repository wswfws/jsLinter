"""
Module containing functions for JavaScript linting.

Functions:
- check_for_empty_lines: Check for empty lines in the JavaScript code.

Usage:
from self_types.js_code import JsCode, JsCodeWarning

# Example usage
code = JsCode("let a = 5\n\n")
warnings = check_for_empty_lines(code)
for warning in warnings:
    print(warning)
"""
from self_types.js_code import JsCode, JsCodeWarning


def check_for_empty_lines(js_code: JsCode, max_code_lines_without_empty_line: int) -> list[JsCodeWarning]:
    """
    Check for empty lines in the provided JsCode object and return a list of JsCodeWarning objects for any issues found.

    Args:
        js_code (JsCode): JsCode object containing the code to be checked for empty lines.
        max_code_lines_without_empty_line (int)

    Returns:
        list[JsCodeWarning]: A list of JsCodeWarning objects highlighting any empty line issues found in the code.
    """

    def get_is_empty_arr(code_lines):
        return [line.strip() == "" for line in code_lines]

    def check_double_empty_lines(is_empty_arr):
        warning_lines = []
        for idx in range(1, len(is_empty_arr)):
            if is_empty_arr[idx] and is_empty_arr[idx - 1]:
                warning_lines.append(idx)

        return warning_lines

    def check_many_code_without_empty_lines(is_empty_arr):
        if len(is_empty_arr) <= max_code_lines_without_empty_line:
            return []

        warning_lines = []
        window_sum = max_code_lines_without_empty_line - sum(is_empty_arr[:max_code_lines_without_empty_line])
        if window_sum >= max_code_lines_without_empty_line:
            warning_lines.append(0)

        for idx in range(1, len(is_empty_arr) - max_code_lines_without_empty_line):
            window_sum += is_empty_arr[idx] - is_empty_arr[idx + max_code_lines_without_empty_line]
            if window_sum >= max_code_lines_without_empty_line:
                warning_lines.append(idx)

        return warning_lines

    warnings: list[JsCodeWarning] = []
    empty_lines = get_is_empty_arr(js_code.line_code)

    for line_num in check_double_empty_lines(empty_lines):
        warnings.append(JsCodeWarning("Extra empty line", js_code.filename, line_num))

    for line_num in check_many_code_without_empty_lines(empty_lines):
        warnings.append(JsCodeWarning("Too much code without an empty line", js_code.filename, line_num))

    return warnings

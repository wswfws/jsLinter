"""
Module for checking spacing style in JavaScript code.

Functions:
- check_before_spacing: Check and report missing space before an operator.
- check_no_before_spacing: Check and report unnecessary space before an operator.
- check_after_spacing: Check and report missing space after an operator.
- check_no_after_spacing: Check and report unnecessary space after an operator.
- check_spaces_style: Check and report spacing style issues in JavaScript code.

Usage:
from self_types.js_code import JsCode, JsCodeWarning

# Example usage
code = JsCode("let a = 5")
config = {
    "before": ["+", "-"],
    "no-before": ["==", "!="],
    "after": ["=", ":"],
    "no-after": [","]
}
warnings = check_spaces_style(code, config)
for warning in warnings:
    print(warning)
"""

from self_types.js_code import JsCode, JsCodeWarning


def check_before_spacing(js_code: JsCode, operator: str, line_num: int) -> JsCodeWarning | None:
    """
    Check and report missing space before an operator.

    Args:
        js_code (JsCode): The JavaScript code to analyze.
        operator (str): The operator to check for spacing.
        line_num (int): The line number in the code to check.

    Returns:
        JsCodeWarning: A warning if missing space is found; None otherwise.
    """
    if line_num < 0 or line_num >= len(js_code.line_code):
        return None
    line = js_code.line_code[line_num]
    if operator in line and line.index(operator) > 0 and line[line.index(operator) - 1] != ' ':
        return JsCodeWarning(f"Add space before {operator} operator", js_code.filename, line_num)
    return None


def check_no_before_spacing(js_code: JsCode, operator: str, line_num: int) -> JsCodeWarning | None:
    """
    Check and report unnecessary space before an operator.

    Args:
        js_code (JsCode): The JavaScript code to analyze.
        operator (str): The operator to check for spacing.
        line_num (int): The line number in the code to check.

    Returns:
        JsCodeWarning: A warning if unnecessary space is found; None otherwise.
    """
    if line_num < 0 or line_num >= len(js_code.line_code):
        return None
    line = js_code.line_code[line_num]
    if operator in line and line.index(operator) > 0 and line[line.index(operator) - 1] == ' ':
        return JsCodeWarning(f"Remove space before {operator}", js_code.filename, line_num)
    return None


def check_after_spacing(js_code: JsCode, operator: str, line_num: int) -> JsCodeWarning | None:
    """
    Check and report missing space after an operator.

    Args:
        js_code (JsCode): The JavaScript code to analyze.
        operator (str): The operator to check for spacing.
        line_num (int): The line number in the code to check.

    Returns:
        JsCodeWarning: A warning if missing space is found; None otherwise.
    """
    if line_num < 0 or line_num >= len(js_code.line_code):
        return None
    line = js_code.line_code[line_num]
    if operator in line and line.index(operator) < len(line) - 1 and line[line.index(operator) + 1] != ' ':
        return JsCodeWarning(f"Add space after {operator} operator", js_code.filename, line_num)
    return None


def check_no_after_spacing(js_code: JsCode, operator: str, line_num: int) -> JsCodeWarning | None:
    """
    Check and report unnecessary space after an operator.

    Args:
        js_code (JsCode): The JavaScript code to analyze.
        operator (str): The operator to check for spacing.
        line_num (int): The line number in the code to check.

    Returns:
        JsCodeWarning: A warning if unnecessary space is found; None otherwise.
    """
    if line_num < 0 or line_num >= len(js_code.line_code):
        return None
    line = js_code.line_code[line_num]
    if operator in line and line.index(operator) < len(line) - 1 and line[line.index(operator) + 1] == ' ':
        return JsCodeWarning(f"Remove space after {operator}", js_code.filename, line_num)
    return None


def check_spaces_style(js_code: JsCode, config: dict[str, list[str]]) -> list[JsCodeWarning]:
    """
    Check and report spacing style issues in JavaScript code, ensuring no duplicate checks
    for overlapping operators.

    Args:
        js_code (JsCode): The JavaScript code to analyze.
        config (dict[str, list[str]]): A configuration dictionary with keys
            'before', 'no-before', 'after', and 'no-after' containing lists of operators to check for spacing.

    Returns:
        list[JsCodeWarning]: A list of warnings for spacing style issues found in the JavaScript code.
    """
    warnings: list[JsCodeWarning | None] = []
    error_positions = []  # Track positions where errors have been detected

    sorted_config = {
        "before": sorted(config.get("before", []), key=len, reverse=True),
        "no-before": sorted(config.get("no-before", []), key=len, reverse=True),
        "after": sorted(config.get("after", []), key=len, reverse=True),
        "no-after": sorted(config.get("no-after", []), key=len, reverse=True)
    }

    # Combine all sorted operators for a single pass per line
    sorted_config = sum([
        [("before", i) for i in sorted_config["before"]],
        [("no-before", i) for i in sorted_config["no-before"]],
        [("after", i) for i in sorted_config["after"]],
        [("no-after", i) for i in sorted_config["no-after"]]
    ], start=[])

    for line_num, line in enumerate(js_code.line_code):
        for op_type, op in sorted_config:
            start_index = line.find(op)

            # Skip if operator not found in line
            if start_index == -1:
                continue

            end_index = start_index + len(op)

            # Check if the error overlaps with an existing recorded error
            if any(start <= start_index < end or start < end_index <= end for (ln, start, end) in error_positions if
                   ln == line_num):
                continue  # Skip already covered positions

            # Depending on operator type, call the relevant spacing check function
            if op_type == "before":
                warning = check_before_spacing(js_code, op, line_num)
            elif op_type == "no-before":
                warning = check_no_before_spacing(js_code, op, line_num)
            elif op_type == "after":
                warning = check_after_spacing(js_code, op, line_num)
            elif op_type == "no-after":
                warning = check_no_after_spacing(js_code, op, line_num)
            else:
                warning = None

            if warning:
                warnings.append(warning)
                error_positions.append((line_num, start_index, end_index))

    return [warning for warning in warnings if warning is not None]

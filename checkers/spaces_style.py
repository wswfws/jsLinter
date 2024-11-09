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

    sorted_config = {
        "before": sorted(config.get("before", []), key=len, reverse=True),
        "no-before": sorted(config.get("no-before", []), key=len, reverse=True),
        "after": sorted(config.get("after", []), key=len, reverse=True),
        "no-after": sorted(config.get("no-after", []), key=len, reverse=True)
    }

    sorted_config = sum([
        [("before", i) for i in sorted_config["before"]],
        [("no-before", i) for i in sorted_config["no-before"]],
        [("after", i) for i in sorted_config["after"]],
        [("no-after", i) for i in sorted_config["no-after"]]
    ], start=[])

    for token in js_code.tokenize_code:
        for op_type, op in sorted_config:
            warning = None
            if token.value != op:
                continue

            if op_type == "before":
                if (
                        token.loc.start.column != 0 and
                        js_code.line_code[token.loc.start.line - 1][token.loc.start.column - 1] != " "
                ):
                    warning = JsCodeWarning(
                        f"Add space before {op} operator",
                        js_code.filename,
                        token.loc.start.line
                    )
            elif op_type == "no-before":
                if (
                        token.loc.start.column != 0 and
                        js_code.line_code[token.loc.start.line - 1][token.loc.start.column - 1] == " "
                ):
                    warning = JsCodeWarning(
                        f"Remove space before {op} operator",
                        js_code.filename,
                        token.loc.start.line
                    )
            elif op_type == "after":
                if (
                        token.loc.end.column < len(js_code.line_code[token.loc.end.line - 1]) and
                        js_code.line_code[token.loc.end.line - 1][token.loc.end.column] != " "
                ):
                    warning = JsCodeWarning(
                        f"Add space after {op} operator",
                        js_code.filename,
                        token.loc.start.line
                    )
            elif op_type == "no-after":
                if (
                        token.loc.end.column < len(js_code.line_code[token.loc.end.line - 1]) and
                        js_code.line_code[token.loc.end.line - 1][token.loc.end.column] == " "
                ):
                    warning = JsCodeWarning(
                        f"Remove space after {op} operator",
                        js_code.filename,
                        token.loc.start.line
                    )

            if warning:
                warnings.append(warning)

    return [warning for warning in warnings if warning is not None]

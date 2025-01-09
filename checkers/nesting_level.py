"""
Module containing functions for max nesting level.
"""

from self_types.js_code import JsCodeWarning, JsCode


def check_for_nesting_level(js_code: JsCode, max_lvl: int) -> list[JsCodeWarning]:
    """
    Check for max nesting level in the JavaScript code.

    Args:
        max_lvl (int): Max nesting level. Must be greater than 0

    Returns:
        list[JsCodeWarning]: A list of JsCodeWarning objects warnings.
    """

    if max_lvl <= 0:
        raise ValueError("max_lvl must be greater than 0")

    warnings: list[JsCodeWarning] = []
    lvl = 0
    last_error_line = -1

    for token in js_code.tokenize_code:
        if token.value in "([{<":
            lvl += 1
            if lvl > max_lvl and last_error_line != token.loc.start.line:
                warnings.append(JsCodeWarning(
                    f"Max nesting level is {max_lvl}, but now is {lvl}.",
                    js_code.filename,
                    token.loc.start.line
                ))
                last_error_line = token.loc.start.line
        elif token.value in ")]}>":
            lvl -= 1
    return warnings

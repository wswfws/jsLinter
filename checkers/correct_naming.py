"""
Module containing functions for checking naming conventions in JavaScript code.

Functions:
- check_for_correct_naming: Main function that validates naming conventions for
    variables, constants, functions, and classes.
- check_variable_naming: Helper to check variable names.
- check_constant_naming: Helper to check constant variable names.
- check_function_naming: Helper to check function names.
- check_class_naming: Helper to check class names.

Usage:
from self_types.js_code import JsCode, JsCodeWarning

# Example usage
code = JsCode("let myVar = 5; const MY_CONST = 10;")
config = {
    "js-variable-pattern": r"^[a-z][a-zA-Z0-9]*$",
    "js-const-variable-pattern": r"^[A-Z_]+$",
    "js-function-pattern": r"^[a-z][a-zA-Z0-9]*$",
    "js-class-pattern": r"^[A-Z][a-zA-Z0-9]*$"
}
warnings = check_for_correct_naming(code, config)
for warning in warnings:
    print(warning)
"""
import re
from contextlib import suppress

from public_props import get_public_props
from self_types.js_code import JsCode, JsCodeWarning


def check_for_correct_naming_variable(
        node, js_variable_pattern, js_const_variable_pattern, filename: str
) -> list[JsCodeWarning]:
    """
    Checks naming conventions for variables and constants in JavaScript code.

    Args:
        node: The AST node representing a variable declaration.
        js_variable_pattern (str): Regex pattern for standard variable names (e.g., lowerCamelCase).
        js_const_variable_pattern (str): Regex pattern for constant variable names (e.g., UPPER_CASE).
        filename (str): The name of the file being checked.

    Returns:
        list[JsCodeWarning]: List of JsCodeWarning objects for any violations found in variable names.
    """
    warnings: list[JsCodeWarning] = []
    if node.kind == "var":
        warnings.append(JsCodeWarning("shouldn't use Var", filename, node.loc.start.line))
    if node.kind == "const":
        for naming in node.declarations:
            name = naming.id.name
            if not re.match(js_const_variable_pattern, name):
                warnings.append(JsCodeWarning(
                    f"const name {name} not in pattern {js_const_variable_pattern}",
                    filename,
                    node.loc.start.line
                ))
    else:
        for naming in node.declarations:
            name = naming.id.name
            if not re.match(js_variable_pattern, name):
                warnings.append(JsCodeWarning(
                    f"variable name {name} not in pattern {js_variable_pattern}",
                    filename,
                    node.loc.start.line
                ))
    return warnings


def check_for_correct_naming_functions(node, js_function_pattern: str, filename: str) -> list[JsCodeWarning]:
    """
    Checks naming conventions for functions in JavaScript code.

    Args:
        node: The AST node representing a function declaration.
        js_function_pattern (str): Regex pattern for function names (e.g., lowerCamelCase).
        filename (str): The name of the file being checked.

    Returns:
        list[JsCodeWarning]: List of JsCodeWarning objects for any violations found in function names.
    """
    warnings: list[JsCodeWarning] = []
    name = node.id.name
    if not re.match(js_function_pattern, name):
        warnings.append(JsCodeWarning(
            f"function name {name} not in pattern {js_function_pattern}",
            filename,
            node.loc.start.line
        ))
    return warnings


def check_for_correct_naming_classes(node, js_class_pattern: str, filename: str) -> list[JsCodeWarning]:
    """
    Checks naming conventions for classes in JavaScript code.

    Args:
        node: The AST node representing a class declaration.
        js_class_pattern (str): Regex pattern for class names (e.g., PascalCase).
        filename (str): The name of the file being checked.

    Returns:
        list[JsCodeWarning]: List of JsCodeWarning objects for any violations found in class names.
    """
    warnings: list[JsCodeWarning] = []
    name = node.id.name
    if not re.match(js_class_pattern, name):
        warnings.append(JsCodeWarning(
            f"class name {name} not in pattern {js_class_pattern}",
            filename,
            node.loc.start.line

        ))
    return warnings


def check_for_correct_naming(js_code: JsCode, config: dict[str, str]) -> list[JsCodeWarning]:
    """
    Check for correct naming conventions in JavaScript code, returning warnings for any violations.

    Args:
        js_code (JsCode): The JavaScript code to be checked, encapsulated in a JsCode object.
        config (dict[str, str]): A dictionary of regex patterns to enforce naming conventions, with keys:
            - "js-variable-pattern": Pattern for variable names (e.g., lowerCamelCase).
            - "js-const-variable-pattern": Pattern for constant variables (e.g., UPPER_CASE).
            - "js-function-pattern": Pattern for function names (e.g., lowerCamelCase).
            - "js-class-pattern": Pattern for class names (e.g., PascalCase).

    Returns:
        list[JsCodeWarning]: A list of JsCodeWarning objects, each representing a naming convention issue.
    """
    js_variable_pattern = config.get("js-variable-pattern", None)
    js_const_variable_pattern = config.get("js-const-variable-pattern", None)
    js_function_pattern = config.get("js-function-pattern", None)
    js_class_pattern = config.get("js-class-pattern", None)

    warnings: list[JsCodeWarning] = []

    def check(body):
        for node in body:
            for inside in get_public_props(node):
                with suppress(AttributeError, TypeError):
                    check(getattr(node, inside).body)
            if node.type == "VariableDeclaration":
                warnings.extend(check_for_correct_naming_variable(
                    node, js_variable_pattern, js_const_variable_pattern, js_code.filename))
            elif node.type == "FunctionDeclaration":
                warnings.extend(check_for_correct_naming_functions(node, js_function_pattern, js_code.filename))
            elif node.type == "ClassDeclaration":
                warnings.extend(check_for_correct_naming_classes(node, js_class_pattern, js_code.filename))

    check(js_code.parsed_code.body)
    return warnings

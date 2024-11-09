import re

from self_types.js_code import JsCode, JsCodeWarning

js_variable_pattern = r"[a-z][A-Za-z]*"


def check_for_correct_naming(js_code: JsCode) -> list[JsCodeWarning]:
    warnings: list[JsCodeWarning] = []

    def check(body):
        for node in body:
            if node.type == "FunctionDeclaration":
                check(node.body.body)
                continue
            if node.type == "VariableDeclaration":
                if node.kind == "var":
                    warnings.append(JsCodeWarning("shouldn't use Var", js_code.filename, node.loc.start.line))
                for naming in node.declarations:
                    name = naming.id.name
                    if not re.match(js_variable_pattern, name):  # todo in config
                        warnings.append(JsCodeWarning(
                            f"variable {name} not in pattern {js_variable_pattern}",
                            js_code.filename,
                            node.loc.start.line
                        ))

    check(js_code.parsed_code.body)
    return warnings

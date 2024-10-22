import esprima


class SimpleJSLinter:
    def __init__(self, code):
        self.code = code
        self.line_code = code.split("\n")
        self.errors = []

    def lint(self):
        try:
            # Парсим код с опцией 'loc' для получения местоположения ошибок
            parsed_code = esprima.parseScript(self.code, tolerant=True, loc=True)
            self.check_for_console_logs(parsed_code.body)
            self.check_for_missing_semicolons(parsed_code.body)
        except esprima.Error as e:
            self.errors.append(f"Parsing error: {e.message}")

    def check_for_console_logs(self, body):
        for node in body:
            if node.type == "FunctionDeclaration":
                self.check_for_console_logs(node.body.body)

            if node.type == "ExpressionStatement" and node.expression.type == "CallExpression":
                callee = node.expression.callee
                if callee.type == "MemberExpression" and callee.object.name == "console":
                    self.errors.append(f"Warning: Console log found on line {node.loc.start.line}")

    def check_for_missing_semicolons(self, body):
        for node in body:
            if node.type == "FunctionDeclaration":
                self.check_for_missing_semicolons(node.body.body)
                continue
            # Проверяем исходный код на наличие точки с запятой
            expression_code = self.line_code[node.loc.start.line - 1:node.loc.end.line]
            if not expression_code[-1].endswith(';'):
                self.errors.append(f"Error: Missing semicolon on line {node.loc.start.line}")

    def report(self):
        if not self.errors:
            print("No linting errors found!")
        else:
            for error in self.errors:
                print(error)


# Пример использования:
js_code = """
let a = 5
console.log(a)
"""

with open("test1.js", "r") as f:
    js_code = f.read()

linter = SimpleJSLinter(js_code)
linter.lint()
linter.report()

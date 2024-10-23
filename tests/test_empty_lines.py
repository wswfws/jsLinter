import unittest

from checkers.empty_lines import check_for_empty_lines, MAX_CODE_LINES_WITHOUT_EMPTY_LINE
from self_types.js_code import JsCode


class CheckEmptyLines(unittest.TestCase):
    def test_empty_lines_present(self):
        code_with_empty_lines = JsCode("let a = 5\n\n\n\nconsole.log(a)")
        warnings = check_for_empty_lines(code_with_empty_lines)
        self.assertEqual(len(warnings), 2)
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 2: Extra empty line")
        self.assertEqual(str(warnings[1]), "Warning: no_filename line 3: Extra empty line")

    def test_no_empty_lines(self):
        code = JsCode("function test() {\nconsole.log('testing')\n}")
        warnings = check_for_empty_lines(code)
        self.assertEqual(len(warnings), 0)

    def test_many_code_without_empty_lines(self):
        for extra_lines in range(10):
            code_without_empty_lines = JsCode(
                "\n".join([f"console.log({i});" for i in range(MAX_CODE_LINES_WITHOUT_EMPTY_LINE + extra_lines)])
            )
            warnings = check_for_empty_lines(code_without_empty_lines)
            self.assertEqual(len(warnings), extra_lines)
            for line in range(extra_lines):
                self.assertEqual(
                    str(warnings[line]),
                    f"Warning: no_filename line {line}: Too much code without an empty line"
                )


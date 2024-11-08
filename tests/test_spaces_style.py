import unittest

from checkers.spaces_style import check_spaces_style
from self_types.js_code import JsCode


class TestCheckSpacesStyle(unittest.TestCase):
    def setUp(self):
        self.config = {
            "before": ["+"],
            "no-before": ["=="],
            "after": ["="],
            "no-after": [","]
        }

    def test_missing_space_before_operator(self):
        code = JsCode("let x= 5+2;")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 0: Add space before + operator")

    def test_unnecessary_space_before_operator(self):
        code = JsCode("if (x == 5) {}")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 0: Remove space before ==")

    def test_missing_space_after_operator(self):
        code = JsCode("let x=5;")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 0: Add space after = operator")

    def test_unnecessary_space_after_operator(self):
        code = JsCode("let x = 5, y = 10;")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 0: Remove space after ,")

    def test_no_warnings(self):
        code = JsCode("let x = 5 + 2;")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 0)

    def test_multiple_issues_in_one_line(self):
        code = JsCode("let x=5+2, y=3 == 4;")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 4)
        warnings = list(map(str, warnings))
        self.assertIn("Warning: no_filename line 0: Add space before + operator", warnings)
        self.assertIn("Warning: no_filename line 0: Add space after = operator", warnings)
        self.assertIn("Warning: no_filename line 0: Remove space after ,", warnings)
        self.assertIn("Warning: no_filename line 0: Remove space before ==", warnings)

    def test_no_duplicate_warnings_for_double_operators(self):
        code = JsCode("if (x == 5) {}")
        warnings = check_spaces_style(code, self.config)
        self.assertEqual(len(warnings), 1)  # Только одно предупреждение для "==", а не для "="
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 0: Remove space before ==")


if __name__ == "__main__":
    unittest.main()

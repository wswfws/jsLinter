import unittest
import re
from checkers.correct_naming import check_for_correct_naming
from self_types.js_code import JsCode, JsCodeWarning


class CheckCorrectNaming(unittest.TestCase):
    def setUp(self):
        # Define common config patterns
        self.config = {
            "js-variable-pattern": r"^[a-z][a-zA-Z0-9]*$",
            "js-const-variable-pattern": r"^[A-Z_]+$",
            "js-function-pattern": r"^[a-z][a-zA-Z0-9]*$",
            "js-class-pattern": r"^[A-Z][a-zA-Z0-9]*$"
        }

    def test_variable_naming_convention(self):
        code = JsCode("let myVar = 5; const MY_CONST = 10; var badVar = 20;")
        warnings = check_for_correct_naming(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(str(warnings[0]), "Warning: no_filename line 1: shouldn't use Var")

    def test_const_variable_naming_convention(self):
        code = JsCode("const VALID_CONST = 10; const INVALID_const = 20;")
        warnings = check_for_correct_naming(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertIn("const name INVALID_const not in pattern", str(warnings[0]))

    def test_function_naming_convention(self):
        code = JsCode("function goodFunction() {} function BadFunction() {}")
        warnings = check_for_correct_naming(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertIn("function name BadFunction not in pattern", str(warnings[0]))

    def test_class_naming_convention(self):
        code = JsCode("class GoodClass {} class badClass {}")
        warnings = check_for_correct_naming(code, self.config)
        self.assertEqual(len(warnings), 1)
        self.assertIn("class name badClass not in pattern", str(warnings[0]))

    def test_multiple_violations(self):
        code = JsCode("""
            const BAD_CONST = 5;
            let goodVar = 10;
            var badVar = 15;
            function BadFunc() {}
            class badClass {}
        """)
        warnings = check_for_correct_naming(code, self.config)
        print(warnings)
        self.assertEqual(len(warnings), 3)
        self.assertIn("shouldn't use Var", str(warnings[0]))
        self.assertIn("BadFunc not in pattern", str(warnings[1]))
        self.assertIn("badClass not in pattern", str(warnings[2]))


if __name__ == "__main__":
    unittest.main()

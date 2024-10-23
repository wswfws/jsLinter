import unittest

from checkers.missing_semicolons import check_for_missing_semicolons
from self_types.js_code import JsCode


class CheckMissingSemicolons(unittest.TestCase):

    def test_missing_semicolon_simple(self):
        js_code = JsCode("let a = 1")
        errors = check_for_missing_semicolons(js_code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].lineno, 1)
        self.assertEqual(str(errors[0]), 'Warning: no_filename line 1: Missing semicolon')

    def test_not_missing_semicolon_simple(self):
        js_code = JsCode("let a = 1;")
        errors = check_for_missing_semicolons(js_code)
        self.assertEqual(len(errors), 0)

    def test_missing_semicolon_in_function(self):
        js_code = JsCode("function foo() { return 42 }")
        errors = check_for_missing_semicolons(js_code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].lineno, 1)
        self.assertEqual(str(errors[0]), 'Warning: no_filename line 1: Missing semicolon')

    def test_not_missing_semicolon_in_function(self):
        js_code = JsCode("function foo() { return 42; }")
        errors = check_for_missing_semicolons(js_code)
        self.assertEqual(len(errors), 0)

    def test_missing_semicolons_with_line_break_in_expression(self):
        js_code = JsCode("let result = 10 +\n 20")
        errors = check_for_missing_semicolons(js_code)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].lineno, 1)
        self.assertEqual(str(errors[0]), 'Warning: no_filename line 1: Missing semicolon')


    def test_not_missing_semicolons_with_line_break_in_expression(self):
        js_code = JsCode("let result = 10 +\n 20;")
        errors = check_for_missing_semicolons(js_code)
        self.assertEqual(len(errors), 0)


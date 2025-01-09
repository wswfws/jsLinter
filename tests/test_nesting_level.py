import unittest

from checkers.nesting_level import check_for_nesting_level
from self_types.js_code import JsCode


class CheckCorrectNaming(unittest.TestCase):

    def test_any_ok1(self):
        code = JsCode("let a = 1;")
        warnings = check_for_nesting_level(code, 10)
        self.assertEqual(len(warnings), 0)

    def test_any_ok2(self):
        code = JsCode("""
function formatNumber(num) {
  return 1;
}
""")
        warnings = check_for_nesting_level(code, 1)
        self.assertEqual(len(warnings), 0)

    def test_any_ok3(self):
        code = JsCode("""
function formatNumber(num) {
  return num.toFixed(2);
}
const a = ()=> {
  const b = ()=> {
    return 1;
  };
};
        """)
        warnings = check_for_nesting_level(code, 2)
        self.assertEqual(len(warnings), 0)

    def test_max_lvl_incorrect(self):
        code = JsCode("let a = 1;")
        with self.assertRaises(Exception) as context:
            check_for_nesting_level(code, 0)

        self.assertTrue('max_lvl must be greater than 0' in str(context.exception))

    def test_more_than_max_lvl(self):
        code = JsCode("""
function formatNumber(num) {
  return num.toFixed(2);
}
const a = ()=> {
  const b = ()=> {
    return 1;
  };
};
const a = ()=> {
    ()=>alert(1);
}
1+1+(1+1)+1+(1+(1+1))
        """)
        warnings = check_for_nesting_level(code, 1)
        self.assertEqual(len(warnings), 4)
        for i in range(4):
            self.assertIn("Max nesting level is 1, but now is 2.", str(warnings[0]))


if __name__ == "__main__":
    unittest.main()

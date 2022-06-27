from django.test import TestCase
_test_case = TestCase()

assert_contains = _test_case.assertContains
#  assert_iquals = _test_case.assertEquals
assert_iqual = _test_case.assertEqual
assert_not_contains = _test_case.assertNotContains
assert_json_equal = _test_case.assertJSONEqual


import unittest
from algorithms import one_edit, look_and_say


class TestCases(unittest.TestCase):

    def test_is_one_edit(self):
        one_edit_test_cases = [("this", "thas", True),
                               ("tais", "this", True),
                               ("tabs", "this", False),
                               ("thisaa", "this", False),
                               ("aathis", "this", False),
                               ("thisa", "this", True),
                               ("athis", "this", True),
                               ("tahis", "this", True),
                               ("thaeis", "this", False),
                               ("tish", "this", False)
                               ]
        for w1, w2, res in one_edit_test_cases:
            try:
                self.assertTrue(one_edit.is_one_edit(w1, w2) == res)
            except AssertionError:
                print("%s wasn't one edit away from %s" % (w1, w2))
                raise AssertionError

    def test_look_and_say(self):
        test_cases = [(1, 11),
                      (11, 21),
                      (21, 1211),
                      (1211, 111221)]
        for input, output in test_cases:
            try:
                self.assertTrue(look_and_say.get_say(input) == output)
            except AssertionError:
                print("%s wasn't equal to output %s" % (input, output))
                raise AssertionError


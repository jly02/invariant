import unittest

from invariant import __version__
from invariant.invariant import pre


def testVersion():
    assert __version__ == "0.1.0"


@pre(lambda x: x > 0, lambda y: y > 0)
def add(x: int, y: int):
    return x + y


class TestPre(unittest.TestCase):
    """Collection of tests to verify precondition
    decorator works as intended.
    """

    def testNoFailedCondition(self):
        add(1, 1)

    def testSingleCondition(self):
        self.assertRaises(ValueError, add, -1, 1)

    def testSecondCondition(self):
        self.assertRaises(ValueError, add, 1, -1)


if __name__ == "__main__":
    testVersion()
    unittest.main()

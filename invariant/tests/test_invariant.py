import unittest

import invariant.constants as const
from invariant import __version__
from invariant.exceptions import PreconditionNotMetError
from invariant.invariant import pre


def testVersion():
    assert __version__ == "0.1.0"


@pre(lambda x: x > 0, lambda y: y > 0)
def add(x: int, y: int):
    """Numerical test function, guarantee inputs are positive."""
    return x + y


@pre(lambda l: l != None, lambda ele: const.FREE)
def appendToList(l: list[any], ele: any):
    """Non-numerical test function, guarantee the given list
    is not None-type.
    """
    l.append(ele)
    return l


class TestPre(unittest.TestCase):
    """Collection of tests to verify precondition
    decorator works as intended.
    """

    def testNoFailedCondition(self):
        self.assertEquals(add(1, 1), 2)

    def testSingleCondition(self):
        self.assertRaises(PreconditionNotMetError, add, -1, 1)

    def testSecondCondition(self):
        self.assertRaises(PreconditionNotMetError, add, 1, -1)

    def testNonNumericalCondition(self):
        self.assertRaises(PreconditionNotMetError, appendToList, None, None)

    def testNoFailedNonNumericalCondition(self):
        self.assertEquals(appendToList([], 1), [1])


if __name__ == "__main__":
    testVersion()
    unittest.main()

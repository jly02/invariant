import unittest

import invariant.constants as const
from invariant import __version__
from invariant.exceptions import PreconditionNotMetError
from invariant.invariant import pre


def testVersion():
    assert __version__ == "0.1.0"


class SimpleDB:
    """Simple key-value store to test class method invariants.
    """
    def __init__(self):
        self.data = {}

    @pre(lambda key: key != None, lambda value: const.FREE)
    def set(self, key, value) -> None:
        self.data[key] = value

    @pre(lambda key: key != None)
    def get(self, key) -> None:
        return self.data.get(key)

    @pre(lambda key: key != None)
    def delete(self, key) -> any:
        if key in self.data:
            del self.data[key]
        else:
            print("Key not found.")

    def display(self) -> None:
        print("Database Contents:")
        for key, value in self.data.items():
            print(f"{key}: {value}")


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
        self.assertEqual(add(1, 1), 2)

    def testSingleCondition(self):
        self.assertRaises(PreconditionNotMetError, add, -1, 1)

    def testSecondCondition(self):
        self.assertRaises(PreconditionNotMetError, add, 1, -1)

    def testNonNumericalCondition(self):
        self.assertRaises(PreconditionNotMetError, appendToList, None, None)

    def testNoFailedNonNumericalCondition(self):
        self.assertEqual(appendToList([], 1), [1])

    def testDBSetGood(self):
        db = SimpleDB()
        db.set("name", "Bob")
        self.assertEqual(db.get("name"), "Bob")


if __name__ == "__main__":
    testVersion()
    unittest.main()

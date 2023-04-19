import inspect


def getPreconditions(func) -> list[str]:
    """Returns list of preconditions attached to a function.
    Only works on functions using the @pre tag.

    Args:
        func: the function whose preconditions are to be obtained

    Returns:
        list[str]: list of preconditions with lambda stripped
    """
    pre_cons = inspect.getsourcelines(func)[0][0]  # first line, @pre tag
    pre_cons = pre_cons[5:].strip(")\n")  # remove leading @pre( and ending )\n
    pre_cons = pre_cons.split(",")  # split into seperate lambda function strings
    pre_cons = [s.strip()[7:] for s in pre_cons]  # remove leading spaces and "lambda"
    return pre_cons


class PreconditionNotMetError(Exception):
    """Exception raised when a listed precondition is not met.

    Attributes:
        failed_pre -- list of precondition indices that failed
        func -------- the failing function
    """

    def __init__(self, failed_pre: list[tuple], func) -> None:
        pre_cons = getPreconditions(func)
        message = f"The following preconditions were not met for function '{func.__name__}':\n"
        for idx, arg in failed_pre:
            message += f"       {pre_cons[idx]} FAILED, got: {arg}\n"
        super().__init__(message)


class MissingPreconditionError(Exception):
    """Exception raised when @pre is used without providing
    preconditions for all given parameters.

    Attributes:
        func -- the failing function
    """

    def __init__(self, func) -> None:
        message = f"Missing one or more preconditions in function '{func.__name__}'"
        super().__init__(message)

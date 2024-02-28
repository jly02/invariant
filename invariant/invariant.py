from typing import Callable
from inspect import signature

from .exceptions import MissingPreconditionError, PreconditionNotMetError


def pre(*conds: list[Callable[[any], bool]]):
    """Decorator tag for defining preconditions on an
    arbitrary function. There must be as many preconditions
    given as there are parameters in a function.

    Args:
        *conds: the preconditions to be checked, in the form
            `lambda var: <condition>`

    Raises:
        MissingPreconditionError: if there are any function
            parameters that are not given a precondition
        PreconditionNotFoundError: if any preconditions are
            not met before calling the function
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if list(signature(func).parameters.keys())[0] == "self":
                trimmed_args = args[1:]
            else:
                trimmed_args = args

            # check that preconditions and args match in length
            if len(conds) < len(trimmed_args):
                raise MissingPreconditionError(func)

            # list of all preconditions failed, if there are any
            failed_pre: list[tuple] = []
            pre_con_idx = 0
            for cond, arg in zip(conds, trimmed_args):
                if not cond(arg):
                    failed_pre.append((pre_con_idx, arg))

                pre_con_idx += 1

            if len(failed_pre) > 0:
                raise PreconditionNotMetError(failed_pre, func)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator

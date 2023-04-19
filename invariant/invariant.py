from .exceptions import PreconditionNotMetError


def pre(*conds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            failed_pre: list[tuple] = []
            pre_con_idx = 0
            for cond, arg in zip(conds, args):
                if not cond(arg):
                    failed_pre.append((pre_con_idx, arg))

                pre_con_idx += 1

            if len(failed_pre) > 0:
                raise PreconditionNotMetError(failed_pre, func)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator

def pre(*conds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for cond, arg in zip(conds, args):
                if not cond(arg):
                    raise ValueError("Precondition not met.")

            return func(*args, **kwargs)

        return wrapper

    return decorator

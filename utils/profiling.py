import time
from _warnings import warn


def warn_if_slow(limit: float = 2):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            result = fun(*args, **kwargs)
            run_duration = time.monotonic() - start_time
            if run_duration > limit:
                warn(f"Slow Run ({run_duration:.2} secs): {fun}")
            return  result
        return wrapper
    return decorator


def since():
    nt = time.monotonic()
    yield 0.
    while True:
        ot, nt = nt, time.monotonic()
        yield nt - ot
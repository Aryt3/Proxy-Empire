import functools

def handle_exceptions(func):
    """
    This decorator catches exceptions raised by the function it wraps
    and ensures that the program does not crash.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred in {func.__name__}: {e}")
            # Log Exception
            return None 

    return wrapper
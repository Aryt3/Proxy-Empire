import functools
import asyncio

def handle_exceptions(func):
    """
    This decorator catches exceptions raised by both synchronous
    and asynchronous functions, ensuring the program does not crash.
    """
    
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f'Error occurred in {func.__name__}: {e}')
            # Log Exception
            return None

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'Error occurred in {func.__name__}: {e}')
            # Log Exception
            return None

    # Check if the function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

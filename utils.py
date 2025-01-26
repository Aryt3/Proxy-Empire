import functools
import asyncio

def silence(func):
    '''
    Function to silence any errors from scraping functions etc...
    '''

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return None

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return None
        
    # Check if the function is async
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

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
            print(f'[!] Error occurred in {func.__name__}: {e}')
            return None

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f'[!] Error occurred in {func.__name__}: {e}')
            return None

    # Check if the function is async
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

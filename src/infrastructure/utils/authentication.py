
from functools import wraps

def authenticate(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print("Succeed authentication")
        value = await func(*args, **kwargs)
        return value
    
    return wrapper

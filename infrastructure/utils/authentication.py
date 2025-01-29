
from functools import wraps

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Succeed authentication")
        value = func()
        return value
    
    return wrapper

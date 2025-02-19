import re
from pydantic import BaseModel, Field

class Account:
    _name: str
    _password: str
    
    def __init__(self):
        self._name = "phuxa"
        self._password = "123456"
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if len(name) not in range(3, 9):
            raise ValueError("Length of name must be between 3-8 characters!")
        
        pattern = r'^[a-zA-Z0-9_-]+$'
        if not re.match(pattern, name):
            raise ValueError("Unexpected characters!")
        
        self._name = name

    def set_password(self, password):
        self._password = password
    
    # def set_name(self, name):
    #     self._name = name
    
    # def get_name(self):
    #     return self._name
    
    def get_password(self):
        return self._password

acc = Account()
# name = acc.get_name()
name = acc.name
print(name)
acc.name = "phudinh"
print(acc.name)


from typing import Optional

class Account:
    def __init__(self, id: str, email:Optional[str]=None):
        self.id = id
        self.email = email

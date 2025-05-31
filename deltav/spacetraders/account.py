from datetime import datetime


class Account:
    def __init__(self, id: str, email: str | None = None):
        self.id: str = id
        self.email: str | None = email
        self.token: str = ""
        self.created_at: datetime = datetime.now()

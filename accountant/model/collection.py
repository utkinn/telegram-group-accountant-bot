from datetime import datetime
from typing import Optional


class Collection:
    def __init__(self, name: Optional[str] = None):
        self.name = name or datetime.now().strftime("%d.%m.%Y")
        self.created_at = datetime.now()

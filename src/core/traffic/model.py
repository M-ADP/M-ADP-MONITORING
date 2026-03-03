from datetime import datetime
from dataclasses import dataclass

@dataclass
class Traffic:
    id: int
    start : datetime
    end : datetime
